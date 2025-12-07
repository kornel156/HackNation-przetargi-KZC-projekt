import { Bold, Italic, Underline, List, Undo, Redo, ChevronDown, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function DocumentEditor() {
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
          {/* Header */}
          <div className="text-center mb-8">
            <p className="font-semibold text-foreground">GMINA PRZYKŁADOWA</p>
            <p className="text-sm text-muted-foreground mt-1">
              ul. Przykładowa 1, 00-001 Miasto
            </p>
          </div>

          {/* Title */}
          <div className="text-center mb-8">
            <h1 className="text-xl font-bold text-foreground leading-tight">
              SPECYFIKACJA WARUNKÓW<br />ZAMÓWIENIA
            </h1>
            <p className="text-sm text-muted-foreground mt-2">(SWZ)</p>
            <p className="text-sm text-muted-foreground mt-4">
              nr ref: ZP.271.1.2023
            </p>
          </div>

          {/* Sections */}
          <div className="space-y-6 text-sm leading-relaxed">
            <section>
              <h2 className="font-bold text-foreground mb-3">
                I. NAZWA I ADRES ZAMAWIAJĄCEGO
              </h2>
              <p className="text-foreground text-justify">
                Zamawiającym jest Gmina Przykładowa, NIP: 000-000-00-00, REGON: 000000000. 
                Adres strony internetowej prowadzonego postępowania: 
                https://platformazakupowa.pl/...
              </p>
            </section>

            <section>
              <h2 className="font-bold text-foreground mb-3">
                II. TRYB UDZIELENIA ZAMÓWIENIA
              </h2>
              <p className="text-foreground text-justify">
                Postępowanie prowadzone jest w trybie podstawowym bez negocjacji na podstawie 
                art. 275 pkt 1 ustawy z dnia 11 września 2019 r. Prawo zamówień publicznych 
                (t.j. Dz. U. z 2022 r. poz. 1710 ze zm.), zwanej dalej "ustawą Pzp".
              </p>
            </section>

            <section className="relative">
              <div className="absolute -left-4 -right-4 -top-2 -bottom-2 bg-highlight/50 rounded-lg border-2 border-primary/30" />
              <div className="relative">
                <div className="absolute -right-2 -top-2">
                  <div className="w-6 h-6 bg-primary rounded-full flex items-center justify-center shadow-medium">
                    <Sparkles className="w-3 h-3 text-primary-foreground" />
                  </div>
                </div>
                <h2 className="font-bold text-foreground mb-3">
                  III. OPIS PRZEDMIOTU ZAMÓWIENIA
                </h2>
                <p className="text-foreground text-justify mb-3">
                  1. Przedmiotem zamówienia jest budowa hali sportowej przy Szkole Podstawowej nr 5. 
                  Szczegółowy opis przedmiotu zamówienia stanowi Załącznik nr 1 do SWZ - 
                  Dokumentacja Projektowa.
                </p>
                <p className="text-foreground text-justify">
                  2. Wykonawca zobowiązany jest do zrealizowania zamówienia na zasadach 
                  określonych w Projektowanych Postanowieniach Umowy stanowiących Załącznik nr 2 do SWZ.
                </p>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
  );
}
