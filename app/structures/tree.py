from app.structures.product_node import ProductNode

class Tree:
    def __init__(self):
        self.root = None

    def insert(self, product):
        if self.root is None:
            self.root = ProductNode(product)
        else:
            self.insert_recursive(self.root, product)

    def insert_recursive(self, current_node, product):
        if product["id"] < current_node.product["id"]:
            if current_node.left is None:
                current_node.left = ProductNode(product)
            else:
                self.insert_recursive(current_node.left, product)
        else:
            if current_node.right is None:
                current_node.right = ProductNode(product)
            else:
                self.insert_recursive(current_node.right, product)

    def search(self, product_id):
        return self.search_recursive(self.root, product_id)

    def search_recursive(self, node, product_id):
        if node is None:
            return None

        if product_id == node.product["id"]:
            return node.product

        if product_id < node.product["id"]:
            return self.search_recursive(node.left, product_id)
        else:
            return self.search_recursive(node.right, product_id)

    def inorder(self):
        result = []
        self.inorder_recursive(self.root, result)
        return result

    def inorder_recursive(self, node, result):
        if node:
            self.inorder_recursive(node.left, result)
            result.append(node.product)
            self.inorder_recursive(node.right, result)
