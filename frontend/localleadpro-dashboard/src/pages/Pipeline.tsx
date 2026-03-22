import { useState } from 'react';
import { usePipelineStatus, useTriggerPipeline } from '../hooks/usePipeline';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';

import Modal from '../components/ui/Modal';
import PageHeader from '../components/layout/PageHeader';
import Spinner from '../components/ui/Spinner';
import { formatDate } from '../lib/utils';
import { PIPELINE_STAGES } from '../lib/constants';
import { Search, CheckCircle, Sparkles, Send, BarChart2, TrendingUp, Play, Zap } from 'lucide-react';
import type { PipelineStage } from '../lib/api';

const ICON_MAP: Record<string, React.ElementType> = {
  Search, CheckCircle, Sparkles, Send, BarChart2, TrendingUp,
};

/**
 * The Pipeline page provides manual control and live logging for the AI Lead Generation pipeline.
 * 
 * Users can view the current status of the pipeline, manually trigger specific stages 
 * (such as Discovery, Qualification, or Outreach), or execute a full pipeline run.
 * Real-time logs are displayed to give immediate feedback on the execution progress.
 */
export default function Pipeline() {
  const { data: pipeline } = usePipelineStatus(5000);
  const trigger = useTriggerPipeline();
  const [showConfirm, setShowConfirm] = useState(false);
  const [logEntries, setLogEntries] = useState<string[]>([]);

  const handleRunFull = () => setShowConfirm(true);

  const confirmRun = () => {
    const now = new Date().toLocaleTimeString('en-US', { hour12: false });
    setLogEntries((prev) => [...prev, `[${now}] Pipeline: all | Status: triggered`].slice(-20));
    trigger.mutate('all');
    setShowConfirm(false);
  };

  const handleRunStage = (stage: PipelineStage) => {
    const now = new Date().toLocaleTimeString('en-US', { hour12: false });
    setLogEntries((prev) => [...prev, `[${now}] Stage: ${stage} | Status: triggered`].slice(-20));
    trigger.mutate(stage);
  };

  const isRunning = pipeline?.last_run?.status === 'running';

  return (
    <div className="space-y-6 animate-fade-in">
      <PageHeader title="Pipeline Control" subtitle="Trigger and monitor the AI lead generation pipeline" />

      {/* Status Banner */}
      <div className={`rounded-xl p-6 border ${isRunning ? 'bg-coldscout-teal/5 border-coldscout-teal/30' : 'bg-navy-800 border-white/10'}`}>
        <div className="flex items-center gap-4">
          {isRunning ? (
            <>
              <Spinner size="md" />
              <div>
                <p className="text-coldscout-teal font-display font-semibold">Pipeline Running</p>
                <p className="text-sm text-gray-400">Current stage: {pipeline?.last_run?.stage ?? 'unknown'}</p>
              </div>
            </>
          ) : (
            <div>
              <p className="text-gray-300 font-display font-semibold">Pipeline Idle</p>
              <p className="text-sm text-gray-500 font-mono">
                Last run: {pipeline?.last_run?.at ? formatDate(pipeline.last_run.at) : 'Never'} · 
                Status: {pipeline?.last_run?.status ?? '—'}
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Stage Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {PIPELINE_STAGES.map((stage) => {
          const Icon = ICON_MAP[stage.icon] || Zap;
          const isActive = pipeline?.last_run?.stage === stage.id;

          return (
            <Card key={stage.id} className={isActive ? 'border-coldscout-teal/30' : ''}>
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className={`p-2 rounded-lg ${isActive ? 'bg-coldscout-teal/10' : 'bg-navy-700'}`}>
                    <Icon className={`w-5 h-5 ${isActive ? 'text-coldscout-teal' : 'text-gray-400'}`} />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-white">{stage.label}</h3>
                    <p className="text-xs text-gray-500">{stage.description}</p>
                  </div>
                </div>
              </div>
              <Button
                size="sm"
                variant="outline"
                icon={<Play className="w-3.5 h-3.5" />}
                onClick={() => handleRunStage(stage.id as PipelineStage)}
                loading={trigger.isPending && trigger.variables === stage.id}
              >
                Run Stage
              </Button>
            </Card>
          );
        })}
      </div>

      {/* Run Full Pipeline CTA */}
      <Button
        className="w-full py-4 text-lg"
        icon={<Zap className="w-5 h-5" />}
        onClick={handleRunFull}
        loading={trigger.isPending && trigger.variables === 'all'}
        disabled={isRunning}
      >
        {isRunning ? 'Pipeline Running...' : 'Run Full Pipeline'}
      </Button>

      {/* Live Log */}
      <Card className="bg-navy-950">
        <h3 className="text-xs font-mono text-gray-400 uppercase tracking-wider mb-3">Pipeline Log</h3>
        <div className="bg-navy-900 rounded-lg p-4 max-h-64 overflow-y-auto font-mono text-xs space-y-1">
          {logEntries.length === 0 ? (
            <p className="text-gray-600">No log entries yet. Trigger a pipeline stage to see output.</p>
          ) : (
            logEntries.map((entry, i) => (
              <p key={i} className="text-gray-400">{entry}</p>
            ))
          )}
        </div>
      </Card>

      {/* Confirm Modal */}
      <Modal open={showConfirm} onClose={() => setShowConfirm(false)} title="Run Full Pipeline">
        <p className="text-gray-400 text-sm mb-4">
          This will trigger all pipeline stages sequentially: Discovery → Qualification → 
          Personalization → Outreach → Report. Are you sure?
        </p>
        <div className="flex gap-3 justify-end">
          <Button variant="ghost" onClick={() => setShowConfirm(false)}>Cancel</Button>
          <Button onClick={confirmRun}>Confirm Run</Button>
        </div>
      </Modal>
    </div>
  );
}
