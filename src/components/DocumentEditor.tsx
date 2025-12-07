import { useState } from "react";
import { Pencil, Eye, Save, X, Download, Loader2, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import ReactMarkdown from "react-markdown";
import MDEditor from "@uiw/react-md-editor";
import { generatePdf, downloadPdf } from "./PdfGenerator";
import { toDocx } from "@md2docx/react-markdown";
import { saveAs } from "file-saver";

interface DocumentEditorProps {
  content?: string;
  onContentChange?: (content: string) => void;
}

const defaultMarkdown = `# SPECYFIKACJA WARUNKÓW ZAMÓWIENIA (SWZ)

**GMINA PRZYKŁADOWA**  
ul. Przykładowa 1, 00-001 Miasto

nr ref: ZP.271.1.2023

---

## I. NAZWA I ADRES ZAMAWIAJĄCEGO

Zamawiającym jest **Gmina Przykładowa**, NIP: 000-000-00-00, REGON: 000000000.  
Adres strony internetowej prowadzonego postępowania: https://platformazakupowa.pl/...

## II. TRYB UDZIELENIA ZAMÓWIENIA

Postępowanie prowadzone jest w trybie podstawowym bez negocjacji na podstawie art. 275 pkt 1 ustawy z dnia 11 września 2019 r. *Prawo zamówień publicznych* (t.j. Dz. U. z 2022 r. poz. 1710 ze zm.), zwanej dalej "ustawą Pzp".

## III. OPIS PRZEDMIOTU ZAMÓWIENIA

1. Przedmiotem zamówienia jest **budowa hali sportowej** przy Szkole Podstawowej nr 5. Szczegółowy opis przedmiotu zamówienia stanowi Załącznik nr 1 do SWZ - Dokumentacja Projektowa.

2. Wykonawca zobowiązany jest do zrealizowania zamówienia na zasadach określonych w Projektowanych Postanowieniach Umowy stanowiących Załącznik nr 2 do SWZ.

### Zakres prac obejmuje:

- Roboty przygotowawcze i ziemne
- Fundamenty i konstrukcję budynku
- Instalacje sanitarne i elektryczne
- Wykończenie wewnętrzne i zewnętrzne
- Zagospodarowanie terenu

## IV. TERMIN WYKONANIA ZAMÓWIENIA

Termin realizacji zamówienia: **12 miesięcy** od daty podpisania umowy.
`;

export function DocumentEditor({ content, onContentChange }: DocumentEditorProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedContent, setEditedContent] = useState(content || defaultMarkdown);
  const [isGeneratingPdf, setIsGeneratingPdf] = useState(false);
  const [isGeneratingDocx, setIsGeneratingDocx] = useState(false);
  const displayContent = content || defaultMarkdown;

  const handleEdit = () => {
    setEditedContent(displayContent);
    setIsEditing(true);
  };

  const handleSave = () => {
    if (onContentChange) {
      onContentChange(editedContent);
    }
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditedContent(displayContent);
    setIsEditing(false);
  };

  const handleDownloadPdf = async () => {
    setIsGeneratingPdf(true);
    try {
      const blob = await generatePdf(displayContent);
      downloadPdf(blob, 'dokument-swz.pdf');
    } catch (error) {
      console.error('Błąd podczas generowania PDF:', error);
    } finally {
      setIsGeneratingPdf(false);
    }
  };

  const handleDownloadDocx = async () => {
    setIsGeneratingDocx(true);
    try {
      const blob = await toDocx(displayContent);
      saveAs(blob, 'dokument-swz.docx');
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
            >
              <Pencil className="w-4 h-4" />
              Edytuj
            </Button>
            <Button 
              variant="outline" 
              size="sm" 
              className="gap-2"
              onClick={handleDownloadPdf}
              disabled={isGeneratingPdf}
            >
              {isGeneratingPdf ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Download className="w-4 h-4" />
              )}
              Pobierz PDF
            </Button>
            <Button 
              variant="outline" 
              size="sm" 
              className="gap-2"
              onClick={handleDownloadDocx}
              disabled={isGeneratingDocx}
            >
              {isGeneratingDocx ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <FileText className="w-4 h-4" />
              )}
              Pobierz DOCX
            </Button>
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
          Ostatnia zmiana: chwile temu
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
              <article className="prose prose-sm max-w-none dark:prose-invert prose-headings:text-foreground prose-p:text-foreground prose-strong:text-foreground prose-li:text-foreground">
                <ReactMarkdown>{displayContent}</ReactMarkdown>
              </article>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
