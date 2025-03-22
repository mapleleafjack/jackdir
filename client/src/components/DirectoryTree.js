import React, { useState } from 'react';

const DirectoryTree = ({ data, selectedPaths, onToggle }) => {
  const [isOpen, setIsOpen] = useState(true);
  const isChecked = selectedPaths.has(data.path);

  return (
    <ul className="uk-list uk-list-collapse">
      <li>
        <div className="uk-grid-small" data-uk-grid>
          <div className="uk-width-auto">
            {data.type === 'directory' && (
              <button
                className="uk-icon-button"
                onClick={() => setIsOpen(!isOpen)}
                data-uk-icon={`icon: ${isOpen ? 'minus' : 'plus'}`}
              />
            )}
          </div>
          <div className="uk-width-auto">
            <input 
              className="uk-checkbox"
              type="checkbox"
              checked={isChecked}
              onChange={(e) => onToggle(data, e.target.checked)}
            />
          </div>
          <div className="uk-width-expand">
            <span className="uk-margin-small-left">
              {data.type === 'directory' ? '📁' : '📄'} {data.name}
            </span>
          </div>
        </div>
        {isOpen && data.children && data.children.length > 0 && (
          <div className="uk-margin-left">
            {data.children.map(child => (
              <DirectoryTree 
                key={child.path} 
                data={child} 
                selectedPaths={selectedPaths} 
                onToggle={onToggle} 
              />
            ))}
          </div>
        )}
      </li>
    </ul>
  );
};

export default DirectoryTree;