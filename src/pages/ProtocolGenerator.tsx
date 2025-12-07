import { Header } from "@/components/Header";
import { ProtocolParametersPanel } from "@/components/ProtocolParametersPanel";
import { ProtocolDocumentEditor } from "@/components/ProtocolDocumentEditor";
import { ProtocolChatPanel } from "@/components/ProtocolChatPanel";
import { useState, useEffect } from "react";

const ProtocolGenerator = () => {
  const [documentContent, setDocumentContent] = useState<string>("");
  const [protocolData, setProtocolData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Szablon początkowy protokołu
  useEffect(() => {
    const initialTemplate = generateInitialProtocolTemplate();
    setDocumentContent(initialTemplate);
    setIsLoading(false);
  }, []);

  const generateInitialProtocolTemplate = () => {
    return `# PROTOKÓŁ POSTĘPOWANIA O UDZIELENIE ZAMÓWIENIA PUBLICZNEGO

## I. INFORMACJE PODSTAWOWE

**Numer postępowania:** ...............
**Nazwa zamówienia:** ...............
**Tryb postępowania:** ...............
**Podstawa prawna:** ...............

## II. ZAMAWIAJĄCY

**Nazwa zamawiającego:** ...............
**Adres:** ...............
**NIP:** ...............
**REGON:** ...............
**Osoba odpowiedzialna:** ...............

## III. PRZEDMIOT ZAMÓWIENIA

**Rodzaj zamówienia:** (dostawy/usługi/roboty budowlane)
**Kody CPV:** ...............
**Opis przedmiotu zamówienia:**

_Opis przedmiotu zamówienia zostanie uzupełniony..._

**Szacunkowa wartość zamówienia:** ............... PLN netto
**Data ustalenia wartości:** ...............

## IV. TERMINY

**Termin składania ofert:** ...............
**Termin otwarcia ofert:** ...............
**Termin związania ofertą:** ...............
**Termin wykonania zamówienia:** ...............

## V. KRYTERIA OCENY OFERT

**Kryteria:**
- Cena: ...............%
- ...............: ...............%

## VI. ZŁOŻONE OFERTY

| Lp. | Nazwa Wykonawcy | Cena brutto | Punkty | Uwagi |
|-----|-----------------|-------------|--------|-------|
| 1.  | ............... | ............... PLN | ... | ... |
| 2.  | ............... | ............... PLN | ... | ... |
| 3.  | ............... | ............... PLN | ... | ... |

## VII. OCENA OFERT

**Liczba ofert złożonych:** ...............
**Liczba ofert odrzuconych:** ...............
**Oferty odrzucone:**

_Brak ofert odrzuconych / Lista ofert odrzuconych..._

## VIII. WYBÓR NAJKORZYSTNIEJSZEJ OFERTY

**Wybrano ofertę wykonawcy:** ...............
**Cena wybranej oferty:** ............... PLN brutto
**Uzasadnienie wyboru:**

_Uzasadnienie wyboru najkorzystniejszej oferty..._

## IX. INFORMACJE O ŚRODKACH OCHRONY PRAWNEJ

**Informacja o wniesionych odwołaniach:** ...............
**Rozstrzygnięcie odwołań:** ...............

## X. PODPISY

**Data sporządzenia protokołu:** ...............

**Komisja przetargowa:**

| Funkcja | Imię i nazwisko | Podpis |
|---------|-----------------|--------|
| Przewodniczący | ............... | ............... |
| Członek | ............... | ............... |
| Sekretarz | ............... | ............... |

**Zatwierdzam:**

_Kierownik Zamawiającego_

...............
(podpis)

## XI. ZAŁĄCZNIKI

1. Ogłoszenie o zamówieniu
2. Specyfikacja Warunków Zamówienia
3. Oferty wykonawców
4. Protokoły z otwarcia ofert
5. Dokumenty potwierdzające spełnienie warunków
6. ...............
`;
  };

  const handleDocumentUpdate = (newContent: string, newData: any) => {
    setDocumentContent(newContent);
    setProtocolData((prev: any) => ({ ...prev, ...newData }));
  };

  const handleContentChange = (newContent: string) => {
    setDocumentContent(newContent);
  };

  return (
    <div className="h-screen flex flex-col bg-background">
      <Header />
      <div className="flex-1 flex overflow-hidden">
        <ProtocolParametersPanel data={protocolData} />
        <ProtocolDocumentEditor 
          content={documentContent} 
          onContentChange={handleContentChange}
          isLoading={isLoading}
        />
        <ProtocolChatPanel onDocumentUpdate={handleDocumentUpdate} />
      </div>
    </div>
  );
};

export default ProtocolGenerator;
