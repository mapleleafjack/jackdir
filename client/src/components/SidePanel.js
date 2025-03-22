import React from 'react';

const SidePanel = ({
  includeHidden,
  setIncludeHidden,
  handleCopy
}) => {
  return (
    <div>
      <div className="uk-margin">
        <label>
          <input
            className="uk-checkbox"
            type="checkbox"
            checked={includeHidden}
            onChange={e => setIncludeHidden(e.target.checked)}
          />
          {' '}
          Include Hidden
        </label>
      </div>

      <button
        className="uk-button uk-button-secondary uk-width-1-1 uk-margin-top"
        onClick={handleCopy}
      >
        Copy Selected
      </button>
    </div>
  );
};

export default SidePanel;
