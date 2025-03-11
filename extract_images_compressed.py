import rclpy
from rclpy.node import Node
import rosbag2_py
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import CompressedImage
from rclpy.serialization import deserialize_message
import os
import tkinter as tk
from tkinter import filedialog
from rosbag2_py import SequentialReader
from rosbag2_py import StorageOptions
from rosbag2_py import ConverterOptions

class BagImageExtractor(Node):
    def __init__(self, bag_path, image_topic, output_dir, storage_id='mcap'):
        super().__init__("bag_image_extractor")
        self.bridge = CvBridge()
        self.bag_path = bag_path
        self.image_topic = image_topic
        self.output_dir = output_dir
        self.reader = rosbag2_py.SequentialReader()
        self.reader.open(rosbag2_py.StorageOptions(uri=self.bag_path, storage_id=storage_id),
                         rosbag2_py.ConverterOptions(input_serialization_format="cdr",
                                                     output_serialization_format="cdr"))
        self.extract_images()

    def extract_images(self):
        connections = self.reader.get_all_topics_and_types()
        topics = [c.name for c in connections]

        if self.image_topic not in topics:
            self.get_logger().error(f"Topic {self.image_topic} not found in bag!")
            return

        count = 0
        while self.reader.has_next():
            (topic, data, t) = self.reader.read_next()
            if topic == self.image_topic:
                img_msg = deserialize_message(data, CompressedImage)
                cv_image = self.bridge.compressed_imgmsg_to_cv2(img_msg, desired_encoding="bgr8")
                filename = f"{self.output_dir}/frame_{count:05d}.png"
                if count % 20 == 0:
                    cv2.imwrite(filename, cv_image)
                    self.get_logger().info(f"Saved {filename}")
                count += 1

    def deserialize_msg(self, data, msg_type):
        msg = msg_type()
        msg.deserialize(data)
        return msg
def select_bag_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askdirectory(title="Select ROS 2 Bag Directory")
    return file_path

def list_topics(bag_path, storage_id='mcap'):
    reader = SequentialReader()
    storage_options = StorageOptions(uri=bag_path, storage_id=storage_id)
    converter_options = ConverterOptions(input_serialization_format='', output_serialization_format='')

    reader.open(storage_options, converter_options)
    topics = set()

    while reader.has_next():
        (topic, _, _) = reader.read_next()
        topics.add(topic)

    return sorted(topics)
def main():
    rclpy.init()
    bag_path = select_bag_file()
    if not bag_path:
        print("No bag file selected.")
        return
    print("\nChoose the storage format:")
    print("1. db3")
    print("2. mcap")
    storage_choice = input("\nEnter your choice (1 or 2): ").strip()
    storage_choice = "sqlite3" if storage_choice == "1" else "mcap"

    try:
        topics = list_topics(bag_path, storage_choice)
        if not topics:
            print("No topics found in the bag file.")
            return


        print("\nAvailable topics:")
        for i, topic in enumerate(topics, 1):
            print(f"{i}. {topic}")

        topic_index = input("\nEnter the number of the topic you want to select: ").strip()
        
        if not topic_index.isdigit() or not (1 <= int(topic_index) <= len(topics)):
            print("Invalid selection.")
            return

        selected_topic = topics[int(topic_index) - 1]
        print(f"\nYou selected: {selected_topic}")

    except Exception as e:
        print(f"Error: {e}")
    output_dir = bag_path+selected_topic+"_extracted"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    extractor = BagImageExtractor(bag_path, selected_topic, output_dir, storage_choice)
    extractor.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
