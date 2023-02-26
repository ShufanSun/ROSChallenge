#Shufan Sun
#2023-02-26


import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray

class MergeArraysNode(Node):
    def __init__(self):
        super().__init__('merge_arrays_node')
        
        # Define the subscribers
        self.array1_sub = self.create_subscription(
            Int32MultiArray,
            '/input/array1',
            self.array1_callback,
            10
        )
        self.array1_sub
        
        self.array2_sub = self.create_subscription(
            Int32MultiArray,
            '/input/array2',
            self.array2_callback,
            10
        )
        self.array2_sub
        
        # Define the publisher
        self.merged_array_pub = self.create_publisher(Int32MultiArray, '/output/array', 10)

        # Initialize the merged array
        self.merged_array = Int32MultiArray()
        self.published=False

    def array1_callback(self, msg):
        if not self.merged_array.data:
            # If this is the first array received, just copy it to the merged array
            self.merged_array.data = msg.data
        else:
            # Merge the two arrays
            self.merged_array.data = self.merge_sorted_arrays(self.merged_array.data, msg.data)
        # Publish the merged array
        if self.merged_array.data and not self.published:
            # Publish the merged array
            self.merged_array_pub.publish(self.merged_array)
            self.published = True

    def array2_callback(self, msg):
        if not self.merged_array.data:
            # If this is the first array received, just copy it to the merged array
            self.merged_array.data = msg.data
        else:
            # Merge the two arrays
            self.merged_array.data = self.merge_sorted_arrays(self.merged_array.data, msg.data)
        # Publish the merged array
         # Check if both arrays have been received and merged
#        if self.merged_array.data and not self.published:
            # Publish the merged array
            self.get_logger().info(self.merged_array.data)
            self.merged_array_pub.publish(self.merged_array)
            self.published = True

    def merge_sorted_arrays(self, arr1, arr2):
        # Merge two sorted arrays
        merged_arr = []
        i = 0
        j = 0
        while i < len(arr1) and j < len(arr2):
            if arr1[i] < arr2[j]:
                merged_arr.append(arr1[i])
                i += 1
            else:
                merged_arr.append(arr2[j])
                j += 1
        merged_arr += arr1[i:]
        merged_arr += arr2[j:]
        return merged_arr

def main(args=None):
    rclpy.init(args=args)
    node = MergeArraysNode()
    print("hello")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
