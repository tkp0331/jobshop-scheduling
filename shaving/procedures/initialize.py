# -*- coding: utf-8 -*-
from ..tree.nodes import JobNode
from ..tree.balanced_tree import BalancedJobTree


def initialize_sigma_and_xi(job_tree: BalancedJobTree) -> None:
    """Calculate initial value of each job's sigma and xi in balanced binary tree.

    Args:
        job_tree (BalancedJobTree):
            An BalancedJobTree instance whose build_and_set_leaves method already called.

    Note:
        This function initialize each job's sigma and xi in place.
    """
    err_msg = "job_tree must be called 'build_and_set_leaves' method before passed."
    assert isinstance(job_tree.root, JobNode), err_msg

    # initialization starts from leaves
    job_nodes = job_tree.leaves.copy()
    while True:
        job_node = job_nodes.popleft()

        parent_job_node = job_node.parent
        lchild_job_node = job_node.left
        rchild_job_node = job_node.right

        # Calculate sigma, xi and supplementary variable tau
        job_node.tau = lchild_job_node.tau + rchild_job_node.tau + job_node.p
        job_node.sigma = job_node.p + rchild_job_node.tau
        job_node.xi = max(
            lchild_job_node.xi + job_node.sigma,
            job_node.q + job_node.sigma,
            rchild_job_node.xi
        )

        if len(job_nodes) == 0:
            # This block is executed when root node is initialized right before.
            # This algorithm proceeds from leaves to root, so finish initialization.
            return

        # NOTE: the data structure of job_nodes is deque, not set.
        # We need to take measures to initialize twice accidentally.
        if parent_job_node is not job_nodes[-1]:
            job_nodes.append(parent_job_node)
