import React from 'react';

const SidePanel = ({
  includeHidden,
  setIncludeHidden,
  respectGitignore,
  setRespectGitignore,
  handleScan,
  handleCopy
}) => (
  <div className="uk-width-1-4@m uk-padding-small">
    <div className="uk-card uk-card-default uk-card-small uk-card-body">
      <h3 className="uk-card-title">Options</h3>
      <div className="uk-margin">
        <label>
          <input
            className="uk-checkbox"
            type="checkbox"
            checked={includeHidden}
            onChange={(e) => setIncludeHidden(e.target.checked)}
          /> Include Hidden
        </label>
      </div>
      <div className="uk-margin">
        <label>
          <input
            className="uk-checkbox"
            type="checkbox"
            checked={respectGitignore}
            onChange={(e) => setRespectGitignore(e.target.checked)}
          /> Respect .gitignore
        </label>
      </div>
      <button 
        className="uk-button uk-button-primary uk-width-1-1"
        onClick={handleScan}
      >
        Scan
      </button>
      <button 
        className="uk-button uk-button-secondary uk-width-1-1 uk-margin-top"
        onClick={handleCopy}
      >
        Copy Selected
      </button>
    </div>
  </div>
);

export default SidePanel;