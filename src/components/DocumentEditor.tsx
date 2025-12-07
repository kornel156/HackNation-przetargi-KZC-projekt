import { Bold, Italic, Underline, List, Undo, Redo, ChevronDown, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import ReactMarkdown from "react-markdown";

interface DocumentEditorProps {
  content: string;
}

export function DocumentEditor({ content }: DocumentEditorProps) {
  return (
    <div className="flex-1 flex flex-col bg-muted/30 overflow-hidden">
      {/* Toolbar */}
      <div className="h-12 border-b border-border bg-card px-4 flex items-center gap-2 shadow-soft">
        <Button variant="toolbar" size="icon-sm">
          <Undo className="w-4 h-4" />
        </Button>
        <Button variant="toolbar" size="icon-sm">
          <Redo className="w-4 h-4" />
        </Button>
        
        <div className="w-px h-6 bg-border mx-2" />
        
        <Button variant="toolbar" size="sm" className="gap-1">
          Normalny tekst
          <ChevronDown className="w-3 h-3" />
        </Button>
        
        <div className="w-px h-6 bg-border mx-2" />
        
        <Button variant="toolbar" size="icon-sm">
          <Bold className="w-4 h-4" />
        </Button>
        <Button variant="toolbar" size="icon-sm">
          <Italic className="w-4 h-4" />
        </Button>
        <Button variant="toolbar" size="icon-sm">
          <Underline className="w-4 h-4" />
        </Button>
        <Button variant="toolbar" size="icon-sm">
          <List className="w-4 h-4" />
        </Button>
        
        <div className="flex-1" />
        
        <span className="text-xs text-muted-foreground">
          Podgląd na żywo
        </span>
      </div>

      {/* Document Content */}
      <div className="flex-1 overflow-y-auto p-8 scrollbar-thin">
        <div className="max-w-3xl mx-auto bg-card rounded-lg shadow-medium p-12 min-h-[800px] animate-fade-in prose prose-sm max-w-none">
          {content ? (
            <ReactMarkdown>{content}</ReactMarkdown>
          ) : (
            <div className="text-center text-muted-foreground mt-20">
              <Sparkles className="w-12 h-12 mx-auto mb-4 opacity-20" />
              <p>Rozpocznij rozmowę z asystentem, aby wygenerować dokument SWZ.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
