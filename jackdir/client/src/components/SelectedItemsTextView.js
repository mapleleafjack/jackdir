/**
 * Recursively build a subtree containing:
 *  - Any file that is in `selectedPaths`,
 *  - Any folder that has at least one selected file/folder inside it,
 *  - Preserves folder structure so we can show an indented text tree.
 */
function filterTree(node, selectedPaths) {
  // If it's a file, include it only if its path is selected
  if (node.type === "file") {
    return selectedPaths.has(node.path) ? node : null
  }

  // If it's a directory, we need to see if any children qualify
  if (!node.children || node.children.length === 0) {
    // If no children, include the directory only if the directory path is selected
    return selectedPaths.has(node.path) ? node : null
  }

  // Otherwise, recursively filter the children
  const filteredChildren = []
  for (const child of node.children) {
    const filteredChild = filterTree(child, selectedPaths)
    if (filteredChild) {
      filteredChildren.push(filteredChild)
    }
  }

  // If after filtering children, there's at least one child or the folder is selected,
  // we keep this directory node. Otherwise, we omit it (return null).
  if (filteredChildren.length > 0 || selectedPaths.has(node.path)) {
    return {
      ...node,
      children: filteredChildren,
    }
  }
  return null
}

/**
 * Renders the filtered node as a list of text lines, adding indentation per level.
 */
function renderTreeAsText(node, level = 0) {
  const indent = "    ".repeat(level)

  // If directory, append a slash to the name
  const line = node.type === "directory" ? `${indent}${node.name}/` : `${indent}${node.name}`

  let result = [line]

  if (node.children) {
    node.children.forEach((child) => {
      result = result.concat(renderTreeAsText(child, level + 1))
    })
  }

  return result
}

const SelectedItemsTextView = ({ data, selectedPaths }) => {
  // Filter down to just the selected portion of the tree
  const filteredTree = filterTree(data, selectedPaths)

  if (!filteredTree) {
    return (
      <div className="uk-flex uk-flex-center uk-flex-middle uk-text-muted" style={{ height: "200px" }}>
        <div className="uk-text-center">
          <span uk-icon="icon: folder; ratio: 2"></span>
          <p>No items selected.</p>
          <p className="uk-text-small">Click on files or folders in the directory tree to select them.</p>
        </div>
      </div>
    )
  }

  // Build an array of lines, then join them with newlines
  const lines = renderTreeAsText(filteredTree)
  const count = lines.length

  // Use <pre> to preserve spacing/indentation
  return (
    <div>
      <div className="uk-flex uk-flex-between uk-margin-small-bottom">
        <span className="uk-badge">
          {count} item{count !== 1 ? "s" : ""} selected
        </span>
      </div>
      <pre
        className="uk-background-muted uk-padding-small uk-border-rounded"
        style={{
          textAlign: "left",
          maxHeight: "calc(100vh - 150px)",
          overflowY: "auto",
          fontFamily: "Consolas, Monaco, 'Andale Mono', monospace",
          fontSize: "0.9rem",
          lineHeight: "1.5",
        }}
      >
        {lines.join("\n")}
      </pre>
    </div>
  )
}

export default SelectedItemsTextView
