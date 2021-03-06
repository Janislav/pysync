import os
import filecmp
from watchdog.events import FileSystemEventHandler
import shutil

class Dispatch:
    ''' This class represents a synchronization object '''
    def __init__(self, name=''):
        self.name = name
        self.node_list = []
        self.file_copied_count = 0
        self.folder_copied_count = 0

    def add_node(self, node):
        self.node_list.append(node)

    def compare_nodes(self):
        ''' This method takes the nodes in the node_list and compares them '''
        nodeListLength = len(self.node_list)
        for node in self.node_list:
            if self.node_list.index(node) < len(self.node_list) - 1: 
                node2 = self.node_list[self.node_list.index(node) + 1]
                print '\nComparing Node ' + str(self.node_list.index(node)) + ' and Node ' + str(self.node_list.index(node) + 1) + ':'
                self._compare_directories(node.root_path, node2.root_path)

    def _compare_directories(self, left, right):
        ''' This method compares directories. If there is a common directory, the
            algorithm must compare what is inside of the directory by calling this
            recursively.
        '''
        comparison = filecmp.dircmp(left, right)
        if comparison.common_dirs:
            for d in comparison.common_dirs:
                self._compare_directories(os.path.join(left, d), os.path.join(right, d))
        if comparison.left_only:
            self._copy(comparison.left_only, left, right)
        if comparison.right_only:
            self._copy(comparison.right_only, right, left)
        left_newer = []
        right_newer = []
        if comparison.diff_files:
            for d in comparison.diff_files:
                l_modified = os.stat(os.path.join(left, d)).st_mtime
                r_modified = os.stat(os.path.join(right, d)).st_mtime
                if l_modified > r_modified:
                    left_newer.append(d)
                else:
                    right_newer.append(d)
        self._copy(left_newer, left, right)
        self._copy(right_newer, right, left)

    def _copy(self, file_list, src, dest):
        ''' This method copies a list of files from a source node to a destination node '''
        for f in file_list:
            srcpath = os.path.join(src, os.path.basename(f))
            if os.path.isdir(srcpath):
                shutil.copytree(srcpath, os.path.join(dest, os.path.basename(f)))
                self.folder_copied_count = self.folder_copied_count + 1
                print 'Copied directory \"' + os.path.basename(srcpath) + '\" from \"' + os.path.dirname(srcpath) + '\" to \"' + dest + '\"'
            else:
                shutil.copy2(srcpath, dest)
                self.file_copied_count = self.file_copied_count + 1
                print 'Copied \"' + os.path.basename(srcpath) + '\" from \"' + os.path.dirname(srcpath) + '\" to \"' + dest + '\"'

class Node:
    ''' This class represents a node in a dispatch synchronization '''  
    def __init__(self, path, name=''):
        self.name = name
        self.root_path = os.path.abspath(path)
        self.file_list = os.listdir(self.root_path)

class MyHandler(FileSystemEventHandler):

    def __init__(self, source_path=".", target_path=None):
        if target_path == None:
            raise RuntimeError("No target path set!")
        self.source_path = source_path
        self.target_path = target_path

    def on_modified(self, event):
        sync(self.source_path, self.target_path)

def sync(source_path, target_path):
    my_dispatch = Dispatch('aaron')
    node1 = Node(source_path, 'node1')
    node2 = Node(target_path, 'node2')
    my_dispatch.add_node(node1)
    my_dispatch.add_node(node2)
    my_dispatch.compare_nodes()
    print 'Total files copied ' + str(my_dispatch.file_copied_count)
    print 'Total folders copied ' + str(my_dispatch.folder_copied_count)
