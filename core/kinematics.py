# core/kinematics.py
# Pure math / kinematics (no GUI). Works directly on sinumerik_components.KinematicNode.

from __future__ import annotations
from typing import Dict, List, Tuple
import math
import numpy as np
from core import sinumerik_components  # uses your existing KinematicNode / KinematicTree

AXIS_LIN = "AXIS_LIN"
AXIS_ROT = "AXIS_ROT"
OFFSET = "OFFSET"
ROT_CONST = "ROT_CONST"


class KinematicModel:
    """
    Kinematics operating directly on sinumerik_components.KinematicNode.
    - Uses node.type ('AXIS_LIN' / 'AXIS_ROT' / others)
    - Uses node.off_dir_x/y/z and node.a_off
    - Writes absolute position back into node.position (list[3]) and sets node.position_calculated
    - Traversal via node.next (child) and node.parallel (sibling branch at the same parent pose)
    """
    def __init__(self, nodes: Dict[str, sinumerik_components.KinematicNode], root_names: List[str]):
        self.nodes = nodes
        self.root_names = root_names if root_names else []

    @classmethod
    def from_tree(cls, sinu_tree: sinumerik_components.KinematicTree) -> "KinematicModel":
        nodes = getattr(sinu_tree, "node_dict", {})
        root_objs = getattr(sinu_tree, "root_nodes", []) or []
        root_names = [rn.name for rn in root_objs if hasattr(rn, "name")]
        return cls(nodes=nodes, root_names=root_names)

    # ---------- public helpers for GUI ----------
    def get_axis_names(self) -> List[str]:
        out = []
        for n in self.nodes.values():
            t = (n.type or "").upper()
            if "AXIS_LIN" in t or "AXIS_ROT" in t:
                out.append(n.name)
        return out

    def axis_type(self, name: str) -> str:
        n = self.nodes.get(name)
        if not n:
            return ""
        t = (n.type or "").upper()
        if "AXIS_LIN" in t:
            return AXIS_LIN
        if "AXIS_ROT" in t:
            return AXIS_ROT
        return t

    def set_axis_value(self, axis_name: str, value: float) -> None:
        n = self.nodes.get(axis_name)
        if n is not None:
            n.a_off = float(value)

    # ---------- core math ----------
    def calculate_positions(self) -> List[Tuple[np.ndarray, np.ndarray]]:
        """
        Returns link segments [(P_parent, P_node), ...] for plotting and
        writes absolute positions into node.position (list of 3 floats).
        """
        # reset flags & positions
        for n in self.nodes.values():
            n.position_calculated = False
            n.position = [0.0, 0.0, 0.0]

        segments: List[Tuple[np.ndarray, np.ndarray]] = []

        def unit_dir(node: sinumerik_components.KinematicNode) -> np.ndarray:
            v = np.array([float(node.off_dir_x), float(node.off_dir_y), float(node.off_dir_z)], dtype=float)
            norm = np.linalg.norm(v)
            return v / norm if norm > 0 else v

        def rot(axis: np.ndarray, theta_deg: float) -> np.ndarray:
            if np.linalg.norm(axis) == 0:
                return np.eye(3)
            axis = axis / np.linalg.norm(axis)
            theta = math.radians(theta_deg)
            K = np.array([[0, -axis[2], axis[1]],
                          [axis[2], 0, -axis[0]],
                          [-axis[1], axis[0], 0]])
            return np.eye(3) + math.sin(theta) * K + (1 - math.cos(theta)) * (K @ K)

        def dfs(node_name: str, R_parent: np.ndarray, t_parent: np.ndarray, parent_pos: np.ndarray | None):
            node = self.nodes.get(node_name)
            if node is None:
                return

            R = R_parent.copy()
            t = t_parent.copy()

            tpe = (node.type or "").upper()
            if "AXIS_LIN" in tpe:
                # user-driven linear axis
                dir_u = unit_dir(node)
                t = t + R @ (dir_u * float(node.a_off))
            elif "AXIS_ROT" in tpe:
                # user-driven rotational axis
                dir_u = unit_dir(node)
                R = R @ rot(dir_u, float(node.a_off))
            elif "OFFSET" in tpe:
                # constant translation (from original OpenGL logic)
                dir_u = unit_dir(node)
                t = t + R @ (dir_u * float(node.a_off))
            elif "ROT_CONST" in tpe:
                # constant rotation (from original OpenGL logic)
                dir_u = unit_dir(node)
                R = R @ rot(dir_u, float(node.a_off))
            # else: BASE/TCP/unknown -> no transform

            # write back absolute position (as list[3])
            node.position = [float(t[0]), float(t[1]), float(t[2])]
            node.position_calculated = True

            # add segment from parent to me (if parent exists)
            if parent_pos is not None:
                segments.append((parent_pos.copy(), t.copy()))

            # depth-first to 'next' (child) from this node's pose
            nxt = getattr(node, "next", "") or ""
            if nxt:
                dfs(nxt, R, t, t.copy())

            # handle 'parallel' as alternative branch at the same parent pose
            par = getattr(node, "parallel", "") or ""
            if par:
                dfs(par, R_parent, t_parent, parent_pos.copy() if parent_pos is not None else None)

        # Start from each root
        if not self.root_names:
            # fallback: pick nodes with in-degree 0 by 'next'
            indeg = {name: 0 for name in self.nodes}
            for n in self.nodes.values():
                if getattr(n, "next", "") in indeg:
                    indeg[n.next] += 1
            roots = [k for k, d in indeg.items() if d == 0] or list(self.nodes.keys())[:1]
        else:
            roots = self.root_names

        for r in roots:
            dfs(r, np.eye(3), np.zeros(3), None)

        return segments