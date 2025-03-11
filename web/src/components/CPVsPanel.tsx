import { Panel, PanelPosition } from '@xyflow/react';
import useSWR from 'swr';
import { fetcher } from '../utils/api';

// Types
type Device = {
  name: string,
  components: {[name: string]: Component},
  connections: [from: string, to: string][],
  hypotheses?: {[id: string]: Hypothesis},
  annotations?: {
    [id: string]: {
      attack_surface: string,
      effect: string,
      attack_model: string
    }
  }
};

type Component = {
  name: string,
  parameters?: {[name: string]: string | number | boolean | null},
};

type Hypothesis = {
  name: string,
  entry_component?: string | null,
  exit_component?: string | null,
};

export type ActiveCPV = {
  bpId: string;
  index: number;
  path: string[];
} | undefined;

type CPVResult = {
  cpv: {
    name: string, 
    exploit_steps: string[]
  },
  path: {path: string[]},
};

// Props type for the component
interface CPVsPanelProps {
  bpId: string | null;
  device: Device | null;
  position?: PanelPosition;
  activeCPV: ActiveCPV;
  onActiveCPVChange: (cpv: ActiveCPV) => void;
}

// Helper function to render CPVs list
function renderCPVs(
  bpId: string,
  cpvs: CPVResult[],
  activeCPV: ActiveCPV,
  onCPVClick: (cpv: ActiveCPV) => void
) {
  const cpvItems = cpvs.map(({cpv: {name, exploit_steps}, path: {path}}, i) => {
    const isActive = activeCPV && 
                     activeCPV.bpId === bpId && 
                     activeCPV.index === i;
    
    return (
      <li 
        key={i} 
        className={`cursor-pointer hover:text-indigo-600 transition-colors px-2 py-1 rounded ${isActive ? 'bg-indigo-50 dark:bg-indigo-900/30' : ''}`}
        onClick={() => {
          if (isActive) {
            onCPVClick(undefined);
          } else {
            onCPVClick({
              bpId,
              index: i,
              path: path
            });
          }
        }}
      >
        <div className="font-medium">{name}</div>
        {isActive && (
          <>
            {exploit_steps && exploit_steps.length > 0 && (
              <div className="ml-2 mt-2">
                <div className="text-sm">Exploit Steps:</div>
                <ol className="list-decimal list-inside text-sm text-gray-700 dark:text-gray-300 mt-1">
                  {exploit_steps.map((step, idx) => (
                    <li key={idx} className="mb-1">{step}</li>
                  ))}
                </ol>
              </div>
            )}
          </>
        )}
      </li>
    );
  });
  return <ul>{cpvItems}</ul>;
}

// Main component
export const CPVsPanel: React.FC<CPVsPanelProps> = ({
  bpId,
  device,
  position,
  activeCPV,
  onActiveCPVChange
}) => {
  // Define hook at the top level, even if we might not use the data
  const { data, error, isLoading } = useSWR(
    bpId !== null ? `/api/blueprints/${bpId}/cpvs` : null, 
    fetcher
  );

  if (bpId === null || device === null) {
    return <> </>;
  }

  let panelInner;
  if (error) {
    panelInner = <div>Error loading CPVs: {error}</div>;
  } else if (isLoading) {
    panelInner = <div>Loading applicable CPVs...</div>;
  } else if (data) {
    panelInner = renderCPVs(bpId, data as CPVResult[], activeCPV, onActiveCPVChange);
  } else {
    panelInner = <div>No data available</div>;
  }

  return (
    <Panel 
      className="bg-white dark:bg-neutral-900 border-2 border-indigo-600 rounded max-w-md" 
      position={position}
    >
      <div className="flex flex-col max-h-[90vh] overflow-auto">
        <h3 className="text-2xl font-bold sticky top-0 bg-white dark:bg-neutral-900 p-4 pb-2 z-10 flex justify-between items-center">
          CPVs
          <button className="text-sm px-3 py-1 bg-indigo-600 hover:bg-indigo-700 text-white dark:hover:bg-indigo-800 rounded transition-colors shadow-sm">Update</button>
        </h3>
        <div className="p-2 pt-0">
          {panelInner}
        </div>
      </div>
    </Panel>
  );
}; 