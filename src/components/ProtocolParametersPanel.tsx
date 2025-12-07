import { useState } from "react";
import { ChevronDown, Info, Calendar, CheckSquare, Users, FileText } from "lucide-react";
import { cn } from "@/lib/utils";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface AccordionSectionProps {
  icon: React.ReactNode;
  title: string;
  children: React.ReactNode;
  defaultOpen?: boolean;
}

function AccordionSection({ icon, title, children, defaultOpen = false }: AccordionSectionProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className="border border-border rounded-lg bg-card overflow-hidden shadow-card">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-4 py-3 flex items-center justify-between hover:bg-muted/50 transition-colors"
      >
        <div className="flex items-center gap-3">
          <span className="text-primary">{icon}</span>
          <span className="font-medium text-sm text-foreground">{title}</span>
        </div>
        <ChevronDown
          className={cn(
            "w-4 h-4 text-muted-foreground transition-transform duration-200",
            isOpen && "rotate-180"
          )}
        />
      </button>
      <div
        className={cn(
          "overflow-hidden transition-all duration-200",
          isOpen ? "max-h-[500px] opacity-100" : "max-h-0 opacity-0"
        )}
      >
        <div className="px-4 pb-4 pt-2 space-y-4 border-t border-border">
          {children}
        </div>
      </div>
    </div>
  );
}

export function ProtocolParametersPanel({ data }: { data?: any }) {
  return (
    <aside className="w-80 border-r border-border bg-background p-4 flex flex-col gap-4 overflow-y-auto scrollbar-thin">
      <div className="mb-2">
        <h2 className="font-semibold text-foreground">Parametry Protokołu</h2>
        <p className="text-sm text-muted-foreground">Dane postępowania przetargowego</p>
      </div>

      <AccordionSection
        icon={<Info className="w-4 h-4" />}
        title="Informacje o Postępowaniu"
        defaultOpen={true}
      >
        <div className="space-y-3">
          <div>
            <Label htmlFor="procNumber" className="text-xs text-muted-foreground">
              Numer Postępowania
            </Label>
            <Input
              id="procNumber"
              defaultValue={data?.procedure_number || ""}
              placeholder="np. ZP.271.1.2024"
              className="mt-1"
            />
          </div>
          <div>
            <Label htmlFor="procName" className="text-xs text-muted-foreground">
              Nazwa Zamówienia
            </Label>
            <Input
              id="procName"
              defaultValue={data?.procurement_title || ""}
              placeholder="Nazwa zamówienia..."
              className="mt-1"
            />
          </div>
          <div>
            <Label htmlFor="procMode" className="text-xs text-muted-foreground">
              Tryb Postępowania
            </Label>
            <Select defaultValue={data?.procurement_mode || ""}>
              <SelectTrigger className="mt-1">
                <SelectValue placeholder="Wybierz tryb" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="unlimited">Przetarg nieograniczony</SelectItem>
                <SelectItem value="limited">Przetarg ograniczony</SelectItem>
                <SelectItem value="base">Tryb podstawowy</SelectItem>
                <SelectItem value="negotiation">Negocjacje</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </AccordionSection>

      <AccordionSection
        icon={<Calendar className="w-4 h-4" />}
        title="Terminy Postępowania"
      >
        <div className="space-y-3">
          <div>
            <Label htmlFor="submissionDeadline" className="text-xs text-muted-foreground">
              Termin składania ofert
            </Label>
            <Input
              id="submissionDeadline"
              type="datetime-local"
              defaultValue={data?.submission_deadline || ""}
              className="mt-1"
            />
          </div>
          <div>
            <Label htmlFor="openingDate" className="text-xs text-muted-foreground">
              Termin otwarcia ofert
            </Label>
            <Input
              id="openingDate"
              type="datetime-local"
              defaultValue={data?.opening_date || ""}
              className="mt-1"
            />
          </div>
          <div>
            <Label htmlFor="protocolDate" className="text-xs text-muted-foreground">
              Data sporządzenia protokołu
            </Label>
            <Input
              id="protocolDate"
              type="date"
              defaultValue={data?.protocol_date || ""}
              className="mt-1"
            />
          </div>
        </div>
      </AccordionSection>

      <AccordionSection
        icon={<Users className="w-4 h-4" />}
        title="Złożone Oferty"
      >
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm text-foreground">Liczba ofert:</span>
            <span className="text-sm font-medium text-primary">{data?.offers_count || "0"}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-foreground">Oferty odrzucone:</span>
            <span className="text-sm font-medium text-destructive">{data?.rejected_count || "0"}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-foreground">Oferty ważne:</span>
            <span className="text-sm font-medium text-success">{data?.valid_count || "0"}</span>
          </div>
        </div>
      </AccordionSection>

      <AccordionSection
        icon={<CheckSquare className="w-4 h-4" />}
        title="Kryteria Oceny"
      >
        <div className="space-y-3">
          {data?.criteria ? (
            data.criteria.map((c: any, i: number) => (
              <div key={i} className="flex items-center justify-between">
                <span className="text-sm text-foreground">{c.name}</span>
                <span className="text-sm font-medium text-primary">{c.weight}%</span>
              </div>
            ))
          ) : (
            <>
              <div className="flex items-center justify-between">
                <span className="text-sm text-foreground">Cena</span>
                <span className="text-sm font-medium text-primary">60%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-foreground">Inne kryteria</span>
                <span className="text-sm font-medium text-primary">40%</span>
              </div>
            </>
          )}
        </div>
      </AccordionSection>

      <AccordionSection
        icon={<FileText className="w-4 h-4" />}
        title="Wybrana Oferta"
      >
        <div className="space-y-3">
          <div>
            <Label className="text-xs text-muted-foreground">Wybrany Wykonawca</Label>
            <p className="text-sm font-medium text-foreground mt-1">
              {data?.selected_contractor || "Nie wybrano jeszcze"}
            </p>
          </div>
          <div>
            <Label className="text-xs text-muted-foreground">Cena wybranej oferty</Label>
            <p className="text-sm font-medium text-primary mt-1">
              {data?.selected_price ? `${data.selected_price} PLN` : "---"}
            </p>
          </div>
        </div>
      </AccordionSection>
    </aside>
  );
}
