import { useState } from "react";
import { Pencil, Eye, Save, X, Download, Loader2, ChevronDown, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import ReactMarkdown from "react-markdown";
import MDEditor from "@uiw/react-md-editor";
import { generatePdf, downloadPdf } from "./PdfGenerator";
import { toDocx } from "mdast2docx";
import { unified } from "unified";
import remarkParse from "remark-parse";
import { saveAs } from "file-saver";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

interface DocumentEditorProps {
  content: string;
  onContentChange?: (content: string) => void;
}

export function DocumentEditor({ content, onContentChange }: DocumentEditorProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedContent, setEditedContent] = useState(content);
  const [isGeneratingPdf, setIsGeneratingPdf] = useState(false);
  const [isGeneratingDocx, setIsGeneratingDocx] = useState(false);

  const handleEdit = () => {
    setEditedContent(content);
    setIsEditing(true);
  };

  const handleSave = () => {
    if (onContentChange) {
      onContentChange(editedContent);
    }
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditedContent(content);
    setIsEditing(false);
  };

  const handleDownloadPdf = async () => {
    if (!content) return;
    setIsGeneratingPdf(true);
    try {
      const blob = await generatePdf(content);
      downloadPdf(blob, 'dokument-swz.pdf');
    } catch (error) {
      console.error('Błąd podczas generowania PDF:', error);
    } finally {
      setIsGeneratingPdf(false);
    }
  };

  const handleDownloadDocx = async () => {
    if (!content) return;
    setIsGeneratingDocx(true);
    try {
      const mdast = unified().use(remarkParse).parse(content);
      const docxBlob = await toDocx(mdast);
      saveAs(docxBlob as Blob, 'dokument-swz.docx');
    } catch (error) {
      console.error('Błąd podczas generowania DOCX:', error);
    } finally {
      setIsGeneratingDocx(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col bg-muted/30 overflow-hidden">
      {/* Toolbar */}
      <div className="h-12 border-b border-border bg-card px-4 flex items-center gap-2 shadow-soft">
        {isEditing ? (
          <>
            <Button 
              variant="default" 
              size="sm" 
              className="gap-2"
              onClick={handleSave}
            >
              <Save className="w-4 h-4" />
              Zapisz
            </Button>
            <Button 
              variant="outline" 
              size="sm" 
              className="gap-2"
              onClick={handleCancel}
            >
              <X className="w-4 h-4" />
              Anuluj
            </Button>
          </>
        ) : (
          <>
            <Button 
              variant="default" 
              size="sm" 
              className="gap-2"
              onClick={handleEdit}
              disabled={!content}
            >
              <Pencil className="w-4 h-4" />
              Edytuj
            </Button>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button 
                  variant="outline" 
                  size="sm" 
                  className="gap-2"
                  disabled={!content || isGeneratingPdf || isGeneratingDocx}
                >
                  {(isGeneratingPdf || isGeneratingDocx) ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <Download className="w-4 h-4" />
                  )}
                  Pobierz
                  <ChevronDown className="w-3 h-3" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="start">
                <DropdownMenuItem onClick={handleDownloadPdf} disabled={isGeneratingPdf}>
                  <Download className="w-4 h-4 mr-2" />
                  Pobierz PDF
                </DropdownMenuItem>
                <DropdownMenuItem onClick={handleDownloadDocx} disabled={isGeneratingDocx}>
                  <Download className="w-4 h-4 mr-2" />
                  Pobierz DOCX
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </>
        )}
        
        <div className="w-px h-6 bg-border mx-2" />
        
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          {isEditing ? (
            <>
              <Pencil className="w-4 h-4" />
              <span>Tryb edycji</span>
            </>
          ) : (
            <>
              <Eye className="w-4 h-4" />
              <span>Tryb podglądu</span>
            </>
          )}
        </div>
        
        <div className="flex-1" />
        
        <span className="text-xs text-muted-foreground">
          {content ? "Ostatnia zmiana: chwile temu" : "Brak dokumentu"}
        </span>
      </div>

      {/* Document Content */}
      <div className="flex-1 overflow-y-auto scrollbar-thin" data-color-mode="light">
        {isEditing ? (
          <div className="h-full">
            <MDEditor
              value={editedContent}
              onChange={(val) => setEditedContent(val || "")}
              height="100%"
              preview="live"
              className="!border-0"
              visibleDragbar={false}
            />
          </div>
        ) : (
          <div className="p-8">
            <div className="max-w-3xl mx-auto bg-card rounded-lg shadow-medium p-12 min-h-[800px] animate-fade-in">
              {content ? (
                <article className="prose prose-sm max-w-none dark:prose-invert prose-headings:text-foreground prose-p:text-foreground prose-strong:text-foreground prose-li:text-foreground">
                  <ReactMarkdown>{content}</ReactMarkdown>
                </article>
              ) : (
                <div className="text-center text-muted-foreground mt-20">
                  <Sparkles className="w-12 h-12 mx-auto mb-4 opacity-20" />
                  <p>Rozpocznij rozmowę z asystentem, aby wygenerować dokument SWZ.</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
