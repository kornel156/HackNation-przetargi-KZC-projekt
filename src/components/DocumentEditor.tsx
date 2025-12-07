import { Bold, Italic, Underline, List, Undo, Redo, ChevronDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import ReactMarkdown from "react-markdown";

interface DocumentEditorProps {
  content?: string;
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

export function DocumentEditor({ content = defaultMarkdown }: DocumentEditorProps) {
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
          Ostatnia zmiana: chwile temu
        </span>
      </div>

      {/* Document Content */}
      <div className="flex-1 overflow-y-auto p-8 scrollbar-thin">
        <div className="max-w-3xl mx-auto bg-card rounded-lg shadow-medium p-12 min-h-[800px] animate-fade-in">
          <article className="prose prose-sm max-w-none dark:prose-invert prose-headings:text-foreground prose-p:text-foreground prose-strong:text-foreground prose-li:text-foreground">
            <ReactMarkdown>{content}</ReactMarkdown>
          </article>
        </div>
      </div>
    </div>
  );
}
