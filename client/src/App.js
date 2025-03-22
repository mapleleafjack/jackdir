import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import DirectoryTree from './components/DirectoryTree';
import SidePanel from './components/SidePanel';
import UIkit from 'uikit';
import Icons from 'uikit/dist/js/uikit-icons';

UIkit.use(Icons);

function App() {
  const [treeData, setTreeData] = useState(null);
  const [includeHidden, setIncludeHidden] = useState(false);
  const [selectedPaths, setSelectedPaths] = useState(new Set());

  useEffect(() => {
    handleScan();
    // eslint-disable-next-line
  }, [includeHidden]);

  const handleScan = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/tree', {
        path: '.',
        include_hidden: includeHidden,
        respect_gitignore: true,
      });
      setTreeData(response.data.tree);
      setSelectedPaths(new Set());
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleToggle = (node, isChecked) => {
    const newSelected = new Set(selectedPaths);
    const updateNode = (n, checked) => {
      if (checked) {
        newSelected.add(n.path);
      } else {
        newSelected.delete(n.path);
      }
      if (n.children) {
        n.children.forEach(child => updateNode(child, checked));
      }
    };
    updateNode(node, isChecked);
    setSelectedPaths(newSelected);
  };

  const handleCopy = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/copy_selected', {
        selected_paths: Array.from(selectedPaths),
        include_hidden: includeHidden
      });
      // UIkit "toast" style notification
      UIkit.notification({
        message: response.data.message,
        status: 'success',
        pos: 'bottom-right',
        timeout: 3000,
      });
    } catch (error) {
      console.error('Error copying:', error);
    }
  };

  return (
    <div
      className="uk-flex"
      style={{
        height: '100%',
        overflow: 'hidden',
        flexDirection: 'row'
      }}
    >
      {/* Main area (directory tree) */}
      <div className="uk-flex-1 uk-overflow-auto uk-padding-small">
        {treeData && (
          <DirectoryTree
            data={treeData}
            selectedPaths={selectedPaths}
            onToggle={handleToggle}
          />
        )}
      </div>

      {/* Side panel */}
      <div
        style={{
          width: '300px',
          overflow: 'hidden'
        }}
      >
        <div className="uk-overflow-auto uk-padding-small">
          <SidePanel
            includeHidden={includeHidden}
            setIncludeHidden={setIncludeHidden}
            handleCopy={handleCopy}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
