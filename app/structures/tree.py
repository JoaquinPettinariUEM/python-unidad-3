from app.structures.product_node import ProductNode

class Tree:
    def __init__(self):
        self.root = None

    def insert(self, product):
        if self.root is None:
            self.root = ProductNode(product)
        else:
            self._insert_recursive(self.root, product)

    def update(self, product_id, name=None, price=None):
        node = self.search(product_id)
        if node is None:
            return None

        if name is not None:
            node["name"] = name

        if price is not None:
            node["price"] = price

        return node

    def delete(self, product_id):
        self.root = self._delete_recursive(self.root, product_id)

    def search(self, product_id):
        return self._search_recursive(self.root, product_id)

    def in_order(self):
        result = []
        self._in_order_recursive(self.root, result)
        return result

    ## Private functions
    def _insert_recursive(self, current_node, product):
        if product["id"] < current_node.product["id"]:
            if current_node.left is None:
                current_node.left = ProductNode(product)
            else:
                self._insert_recursive(current_node.left, product)
        else:
            if current_node.right is None:
                current_node.right = ProductNode(product)
            else:
                self._insert_recursive(current_node.right, product)

    def _delete_recursive(self, node, product_id):
        if node is None:
            return None

        if product_id < node.product["id"]:
            node.left = self._delete_recursive(node.left, product_id)
        elif product_id > node.product["id"]:
            node.right = self._delete_recursive(node.right, product_id)
        else:
            if node.left is None and node.right is None:
                return None
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            successor = self._min_value_node(node.right)
            node.product = successor.product
            node.right = self._delete_recursive(node.right, successor.product["id"])

        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _search_recursive(self, node, product_id):
        if node is None:
            return None

        if product_id == node.product["id"]:
            return node.product

        if product_id < node.product["id"]:
            return self._search_recursive(node.left, product_id)
        else:
            return self._search_recursive(node.right, product_id)

    def _in_order_recursive(self, node, result):
        if node:
            self._in_order_recursive(node.left, result)
            result.append(node.product)
            self._in_order_recursive(node.right, result)
