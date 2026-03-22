import { useState, useEffect } from 'react';
import { useConfigJobs, useUpdateConfig, useHealth, useSystemToggle } from '../hooks/useConfig';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Toggle from '../components/ui/Toggle';
import JsonEditor from '../components/ui/JsonEditor';
import { PageLoader } from '../components/ui/Spinner';
import PageHeader from '../components/layout/PageHeader';
import Badge from '../components/ui/Badge';
import toast from 'react-hot-toast';
import { Shield, Save, RotateCcw } from 'lucide-react';

/**
 * The Settings page provides global system administration capabilities.
 * 
 * It includes a raw JSON editor for advanced configuration of pipeline jobs (`jobs_config.json`),
 * allowing precise control over worker parameters. It also features a global production 
 * kill-switch to immediately pause or resume all pipeline activities, and displays 
 * high-level system health and security information.
 */
export default function Settings() {
  const { data: jobsConfig, isLoading: jobsLoading } = useConfigJobs();
  const { data: health, isLoading: healthLoading } = useHealth();
  const updateConfig = useUpdateConfig();
  const systemToggle = useSystemToggle();

  const [jsonStr, setJsonStr] = useState('');
  const [dirty, setDirty] = useState(false);

  useEffect(() => {
    if (jobsConfig) {
      const timer = setTimeout(() => {
        setJsonStr(JSON.stringify(jobsConfig, null, 2));
      }, 0);
      return () => clearTimeout(timer);
    }
  }, [jobsConfig]);

  const handleSave = () => {
    try {
      const parsed = JSON.parse(jsonStr);
      updateConfig.mutate(parsed);
      setDirty(false);
    } catch {
      toast.error('Invalid JSON: please fix syntax errors');
    }
  };

  const handleReset = () => {
    if (jobsConfig) {
      setJsonStr(JSON.stringify(jobsConfig, null, 2));
      setDirty(false);
    }
  };

  if (jobsLoading || healthLoading) return <PageLoader />;

  const isRunning = health?.production_status === true;

  return (
    <div className="space-y-6 animate-fade-in">
      <PageHeader title="Settings" subtitle="System configuration and administration" />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Config Editor (2/3) */}
        <div className="lg:col-span-2 space-y-4">
          <Card>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-mono text-gray-400 uppercase tracking-wider">Jobs Configuration</h3>
              <div className="flex items-center gap-2">
                {dirty && <Badge label="Modified" variant="amber" />}
                <Button
                  variant="ghost"
                  size="sm"
                  icon={<RotateCcw className="w-3.5 h-3.5" />}
                  onClick={handleReset}
                  disabled={!dirty}
                >
                  Reset
                </Button>
                <Button
                  size="sm"
                  icon={<Save className="w-3.5 h-3.5" />}
                  onClick={handleSave}
                  loading={updateConfig.isPending}
                  disabled={!dirty}
                >
                  Save
                </Button>
              </div>
            </div>
            <JsonEditor
              value={jsonStr}
              onChange={(v) => { setJsonStr(v); setDirty(true); }}
              height={500}
            />
          </Card>
        </div>

        {/* Sidebar Settings (1/3) */}
        <div className="space-y-4">
          {/* System Toggle */}
          <Card>
            <h3 className="text-sm font-mono text-gray-400 uppercase tracking-wider mb-3">Production Status</h3>
            <div className="flex items-center justify-between py-2">
              <div>
                <p className="text-sm text-white font-medium">
                  System is {isRunning ? 'running' : 'on hold'}
                </p>
                <p className="text-xs text-gray-500">Toggle to hold/resume all scheduled jobs</p>
              </div>
              <Toggle
                value={isRunning}
                onChange={() => systemToggle.mutate(isRunning ? 'hold' : 'resume')}
                disabled={systemToggle.isPending}
              />
            </div>
          </Card>

          {/* Health Info */}
          <Card>
            <h3 className="text-sm font-mono text-gray-400 uppercase tracking-wider mb-3">System Info</h3>
            <div className="space-y-3 text-xs">
              <div className="flex justify-between">
                <span className="text-gray-500">Version</span>
                <span className="font-mono text-coldscout-teal">{health?.version ?? '—'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Status</span>
                <Badge label={health?.status === 'healthy' ? 'Healthy' : 'Error'} variant={health?.status === 'healthy' ? 'green' : 'red'} />
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Scheduler</span>
                <Badge label={health?.scheduler_running ? 'Active' : 'Inactive'} variant={health?.scheduler_running ? 'green' : 'amber'} />
              </div>
            </div>
          </Card>

          {/* Security */}
          <Card>
            <div className="flex items-center gap-2 mb-3">
              <Shield className="w-4 h-4 text-coldscout-teal" />
              <h3 className="text-sm font-mono text-gray-400 uppercase tracking-wider">Security</h3>
            </div>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-gray-500">API Key</span>
                <span className="font-mono text-gray-400">••••••••••</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Auth</span>
                <Badge label="Proxy-side" variant="green" />
              </div>
              <p className="text-gray-600 text-[10px] mt-2">
                API key is stored in the proxy server environment and never exposed to the frontend.
              </p>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
