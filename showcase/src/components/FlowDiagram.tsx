interface Props {
  nodes: string[]
  trigger: string
}

const NODE_W = 140
const NODE_H = 40
const H_GAP = 30
const ROW_GAP = 60
const NODES_PER_ROW = 4
const PADDING = 20

function truncate(text: string, max = 16) {
  return text.length > max ? text.slice(0, max - 1) + '…' : text
}

function isAINode(name: string) {
  const l = name.toLowerCase()
  return l.includes('ai') || l.includes('claude') || l.includes('openai') || l.includes('groq') || l.includes('http request (') || l.includes('parse ai')
}

function nodeColor(name: string, index: number) {
  if (index === 0) return { fill: '#4338ca', stroke: '#6366f1', text: '#e0e7ff' }
  if (isAINode(name)) return { fill: '#065f46', stroke: '#10b981', text: '#a7f3d0' }
  return { fill: '#1f2937', stroke: '#374151', text: '#d1d5db' }
}

export default function FlowDiagram({ nodes }: Props) {
  if (!nodes || nodes.length === 0) return null
  const rows = Math.ceil(nodes.length / NODES_PER_ROW)
  const maxNodesInRow = Math.min(nodes.length, NODES_PER_ROW)
  const svgWidth = maxNodesInRow * NODE_W + (maxNodesInRow - 1) * H_GAP + PADDING * 2
  const svgHeight = rows * NODE_H + (rows - 1) * ROW_GAP + PADDING * 2
  const positions = nodes.map((_, i) => {
    const row = Math.floor(i / NODES_PER_ROW)
    const col = i % NODES_PER_ROW
    const nodesInThisRow = row < rows - 1 ? NODES_PER_ROW : nodes.length - row * NODES_PER_ROW
    const rowStartX = PADDING + ((maxNodesInRow - nodesInThisRow) * (NODE_W + H_GAP)) / 2
    return { x: rowStartX + col * (NODE_W + H_GAP), y: PADDING + row * (NODE_H + ROW_GAP) }
  })
  return (
    <div className="w-full overflow-x-auto">
      <svg viewBox={`0 0 ${svgWidth} ${svgHeight}`} width="100%" style={{maxWidth:svgWidth,display:'block',margin:'0 auto'}} xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="arr" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#6b7280" /></marker>
        </defs>
        {nodes.slice(0,-1).map((_,i) => {
          const from = positions[i], to = positions[i+1]
          const sameRow = Math.floor(i/NODES_PER_ROW) === Math.floor((i+1)/NODES_PER_ROW)
          if (sameRow) return <line key={i} x1={from.x+NODE_W} y1={from.y+NODE_H/2} x2={to.x-8} y2={to.y+NODE_H/2} stroke="#6b7280" strokeWidth="1.5" markerEnd="url(#arr)" />
          const midY = (from.y+NODE_H+to.y)/2
          return <path key={i} d={`M ${from.x+NODE_W/2} ${from.y+NODE_H} C ${from.x+NODE_W/2} ${midY}, ${to.x+NODE_W/2} ${midY}, ${to.x+NODE_W/2} ${to.y-8}`} stroke="#6b7280" strokeWidth="1.5" fill="none" markerEnd="url(#arr)" />
        })}
        {nodes.map((name, i) => {
          const {x,y} = positions[i], colors = nodeColor(name, i)
          return (
            <g key={i}>
              <rect x={x} y={y} width={NODE_W} height={NODE_H} rx={8} fill={colors.fill} stroke={colors.stroke} strokeWidth="1.5" />
              <text x={x+NODE_W/2} y={y+NODE_H/2} textAnchor="middle" dominantBaseline="central" fill={colors.text} fontSize="11" fontFamily="ui-monospace,monospace" fontWeight="500">{truncate(name,17)}</text>
            </g>
          )
        })}
      </svg>
    </div>
  )
}
