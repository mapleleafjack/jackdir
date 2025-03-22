import React from 'react';

/**
 * Recursively build a subtree containing:
 *  - Any file that is in `selectedPaths`,
 *  - Any folder that has at least one selected file/folder inside it,
 *  - Preserves folder structure so we can show an indented text tree.
 */
function filterTree(node, selectedPaths) {
  // If it's a file, include it only if its path is selected
  if (node.type === 'file') {
    return selectedPaths.has(node.path) ? node : null;
  }

  // If it's a directory, we need to see if any children qualify
  if (!node.children || node.children.length === 0) {
    // If no children, include the directory only if the directory path is selected
    return selectedPaths.has(node.path) ? node : null;
  }

  // Otherwise, recursively filter the children
  const filteredChildren = [];
  for (let child of node.children) {
    const filteredChild = filterTree(child, selectedPaths);
    if (filteredChild) {
      filteredChildren.push(filteredChild);
    }
  }

  // If after filtering children, there's at least one child or the folder is selected,
  // we keep this directory node. Otherwise, we omit it (return null).
  if (filteredChildren.length > 0 || selectedPaths.has(node.path)) {
    return {
      ...node,
      children: filteredChildren
    };
  }
  return null;
}

/**
 * Renders the filtered node as a list of text lines, adding indentation per level.
 */
function renderTreeAsText(node, level = 0) {
  const indent = '    '.repeat(level);
  
  // If directory, append a slash to the name
  const line = (node.type === 'directory')
    ? `${indent}${node.name}/`
    : `${indent}${node.name}`;

  let result = [line];

  if (node.children) {
    node.children.forEach(child => {
      result = result.concat(renderTreeAsText(child, level + 1));
    });
  }

  return result;
}

const SelectedItemsTextView = ({ data, selectedPaths }) => {
  // Filter down to just the selected portion of the tree
  const filteredTree = filterTree(data, selectedPaths);

  if (!filteredTree) {
    return <div style={{ color: '#999', marginTop: '1rem' }}>No items selected.</div>;
  }

  // Build an array of lines, then join them with newlines
  const lines = renderTreeAsText(filteredTree);

  // Use <pre> to preserve spacing/indentation
  return (
    <pre style={{ textAlign: 'left', marginTop: '1rem' }}>
      {lines.join('\n')}
    </pre>
  );
};

export default SelectedItemsTextView;
