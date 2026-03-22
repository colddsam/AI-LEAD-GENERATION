import Editor from '@monaco-editor/react';

interface JsonEditorProps {
  value: string;
  onChange: (v: string) => void;
  height?: number;
}

export default function JsonEditor({ value, onChange, height = 400 }: JsonEditorProps) {
  return (
    <div className="rounded-lg overflow-hidden border border-white/10">
      <Editor
        height={`${height}px`}
        defaultLanguage="json"
        theme="vs-dark"
        value={value}
        onChange={(v) => onChange(v || '')}
        options={{
          minimap: { enabled: false },
          fontSize: 13,
          fontFamily: '"JetBrains Mono", monospace',
          scrollBeyondLastLine: false,
          padding: { top: 12, bottom: 12 },
          lineNumbers: 'on',
          renderLineHighlight: 'none',
          wordWrap: 'on',
        }}
      />
    </div>
  );
}
