import React from 'react';
import DirectoryTree from './DirectoryTree';

const MainContent = ({ treeData, selectedPaths, handleToggle }) => (
  <div className="uk-width-3-4@m uk-padding-small">
    <div className="uk-card uk-card-default uk-card-body">
      <h1 className="uk-card-title">Jackdir Interface</h1>
      {treeData && (
        <DirectoryTree 
          data={treeData} 
          selectedPaths={selectedPaths} 
          onToggle={handleToggle} 
        />
      )}
    </div>
  </div>
);

export default MainContent;