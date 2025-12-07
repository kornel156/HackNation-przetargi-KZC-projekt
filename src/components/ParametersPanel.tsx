import { useState } from "react";
import { ChevronDown, Info, Calendar, CheckSquare } from "lucide-react";
import { cn } from "@/lib/utils";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
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

export function ParametersPanel({ data }: { data?: any }) {
  return (
    <aside className="w-80 border-r border-border bg-background p-4 flex flex-col gap-4 overflow-y-auto scrollbar-thin">
      <div className="mb-2">
        <h2 className="font-semibold text-foreground">Parametry Zamówienia</h2>
        <p className="text-sm text-muted-foreground">Wprowadź dane podstawowe</p>
      </div>

      <AccordionSection
        icon={<Info className="w-4 h-4" />}
        title="Informacje Podstawowe"
        defaultOpen={true}
      >
        <div className="space-y-3">
          <div>
            <Label htmlFor="projectName" className="text-xs text-muted-foreground">
              Nazwa Projektu
            </Label>
            <Input
              id="projectName"
              defaultValue={data?.procurement_title || "Budowa hali sportowej przy SP nr 5"}
              className="mt-1"
            />
          </div>
          <div>
            <Label htmlFor="refNumber" className="text-xs text-muted-foreground">
              Numer Referencyjny
            </Label>
            <Input
              id="refNumber"
              defaultValue={data?.procurement_id || "ZP.271.1.2023"}
              className="mt-1 text-muted-foreground"
            />
          </div>
          <div>
            <Label htmlFor="procurementType" className="text-xs text-muted-foreground">
              Tryb Zamówienia
            </Label>
            <Select defaultValue={data?.procurement_mode || "unlimited"}>
              <SelectTrigger className="mt-1">
                <SelectValue placeholder="Wybierz tryb" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="unlimited">Przetarg nieograniczony</SelectItem>
                <SelectItem value="limited">Przetarg ograniczony</SelectItem>
                <SelectItem value="negotiation">Negocjacje z ogłoszeniem</SelectItem>
                <SelectItem value="dialog">Dialog konkurencyjny</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </AccordionSection>

      <AccordionSection
        icon={<Calendar className="w-4 h-4" />}
        title="Terminy i Realizacja"
      >
        <div className="space-y-3">
          <div>
            <Label htmlFor="submissionDate" className="text-xs text-muted-foreground">
              Termin składania ofert
            </Label>
            <Input
              id="submissionDate"
              type="date"
              defaultValue={data?.submission_deadline || "2024-02-15"}
              className="mt-1"
            />
          </div>
          <div>
            <Label htmlFor="executionDate" className="text-xs text-muted-foreground">
              Termin realizacji
            </Label>
            <Input
              id="executionDate"
              type="text"
              defaultValue={data?.execution_deadline || "2024-12-31"}
              className="mt-1"
            />
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
                <span className="text-sm text-foreground">Termin realizacji</span>
                <span className="text-sm font-medium text-primary">20%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-foreground">Gwarancja</span>
                <span className="text-sm font-medium text-primary">20%</span>
              </div>
            </>
          )}
        </div>
      </AccordionSection>
    </aside>
  );
}
