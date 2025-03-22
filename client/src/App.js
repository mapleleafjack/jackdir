import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SidePanel from './components/SidePanel';
import MainContent from './components/MainContent';
import UIkit from 'uikit';
import Icons from 'uikit/dist/js/uikit-icons';

UIkit.use(Icons);

function App() {
  const [treeData, setTreeData] = useState(null);
  const [includeHidden, setIncludeHidden] = useState(false);
  const [respectGitignore, setRespectGitignore] = useState(true);
  const [selectedPaths, setSelectedPaths] = useState(new Set());

  useEffect(() => {
    handleScan();
  }, []);

  const handleScan = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/tree', {
        path: '.',
        include_hidden: includeHidden,
        respect_gitignore: respectGitignore
      });
      setTreeData(response.data.tree);
      setSelectedPaths(new Set());
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleToggle = (node, isChecked) => {
    const newSelected = new Set(selectedPaths);
    const updateNode = (node, checked) => {
      checked ? newSelected.add(node.path) : newSelected.delete(node.path);
      node.children?.forEach(child => updateNode(child, checked));
    };
    updateNode(node, isChecked);
    setSelectedPaths(newSelected);
  };

  const handleCopy = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/copy_selected', {
        selected_paths: Array.from(selectedPaths),
        include_hidden: includeHidden,
        respect_gitignore: respectGitignore
      });
      // UIkit "toast" style notification:
      UIkit.notification({
        message: response.data.message,
        status: 'success',
        pos: 'bottom-right',      // or "bottom-center", etc.
        timeout: 3000          // milliseconds
      });
    } catch (error) {
      console.error('Error copying:', error);
    }
  };

  return (
    <div className="uk-grid uk-grid-small" data-uk-grid>
      <SidePanel
        includeHidden={includeHidden}
        setIncludeHidden={setIncludeHidden}
        respectGitignore={respectGitignore}
        setRespectGitignore={setRespectGitignore}
        handleScan={handleScan}
        handleCopy={handleCopy}
      />
      <MainContent
        treeData={treeData}
        selectedPaths={selectedPaths}
        handleToggle={handleToggle}
      />
    </div>
  );
}

export default App;