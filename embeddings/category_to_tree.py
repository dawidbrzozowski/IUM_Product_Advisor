from typing import List

from treelib import Tree


def get_category_paths_node_split(products) -> List[list]:
    category_paths = get_category_paths(products)
    return _get_paths_split_by_node(category_paths)


def get_category_paths(products) -> set:
    categories = set()
    for product in products:
        categories.add(product['category_path'])
    return categories


def _get_paths_split_by_node(category_paths):
    split_nodes = []
    for category_path in category_paths:
        split_nodes.append(category_path.split(';'))
    return split_nodes


class CategoryTree:

    def __init__(self, products):
        self.category_paths_split = get_category_paths_node_split(products)
        self.tree = self._create_categories_tree()

    def _create_categories_tree(self) -> Tree:
        tree = Tree()
        tree.create_node('root', 'root')
        for category_path_split in self.category_paths_split:
            parent_node = 'root'
            for node in category_path_split:
                if not tree.contains(node):
                    tree.create_node(node, node, parent=parent_node)
                parent_node = node
        return tree

    def get_path_to_leaf(self, leaf: str):
        all_paths = self.tree.paths_to_leaves()
        for path in all_paths:
            if path[-1] == leaf:
                return path
        return None

    def get_descendants_of_node(self, node: str) -> List[str]:
        return [node for node in self.tree.expand_tree(node) if self.tree.get_node(node).is_leaf()]

    def get_all_leafs(self):
        return self.get_descendants_of_node('root')

    def get_leaf_from_category_path(self, category_path):
        category_split = category_path.split(';')
        return category_split[-1]

    def get_leaf2idx(self):
        leaf2idx = {}
        all_leafs = self.get_all_leafs()
        for i, leaf in enumerate(all_leafs):
            leaf2idx[leaf] = i
        return leaf2idx
