import React, { useState } from 'react';
import './DirectoryTree.css'; // Import the CSS file for styles

const DirectoryTree = ({ data, selectedPaths, onToggle }) => {
  const [isOpen, setIsOpen] = useState(true);
  const isSelected = selectedPaths.has(data.path);

  // Toggle selection when clicking the row
  const handleRowClick = () => {
    onToggle(data, !isSelected);
  };

  // Toggle open/closed without triggering row selection
  const toggleOpen = (e) => {
    e.stopPropagation();
    setIsOpen(!isOpen);
  };

  // Order children: directories first then files, both alphabetically by name.
  const sortedChildren =
    data.children &&
    data.children.slice().sort((a, b) => {
      if (a.type === b.type) {
        return a.name.localeCompare(b.name);
      }
      return a.type === 'directory' ? -1 : 1;
    });

  return (
    <div>
      <div 
        className={`tree-row ${isSelected ? 'selected' : ''}`}
        onClick={handleRowClick}
      >
        {/* Reserve space for the toggle button */}
        <div className="toggle-container">
          {data.type === 'directory' && (
            <button className="toggle-button" onClick={toggleOpen}>
              {isOpen ? '-' : '+'}
            </button>
          )}
        </div>
        <span className="icon">
          {data.type === 'directory' ? '📁' : '📄'}
        </span>
        <span className="name">{data.name}</span>
      </div>

      {isOpen && sortedChildren && sortedChildren.length > 0 && (
        <div className="tree-children">
          {sortedChildren.map(child => (
            <DirectoryTree
              key={child.path}
              data={child}
              selectedPaths={selectedPaths}
              onToggle={onToggle}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default DirectoryTree;
