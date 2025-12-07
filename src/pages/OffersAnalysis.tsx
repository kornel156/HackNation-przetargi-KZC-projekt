import { Upload, FileSpreadsheet, AlertCircle, DollarSign, ShieldCheck, Calendar, SlidersHorizontal, ArrowUpDown, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Header } from "@/components/Header";
import EvaluationCriteriaCard from "@/components/EvaluationCriteriaCard";
import OffersTable from "@/components/OffersTable";
import { useRef } from "react";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

const OffersAnalysis = () => {
  const swzFileInputRef = useRef<HTMLInputElement>(null);

  const handleSwzFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      console.log("Pobrano plik SWZ:", file.name, file.type);
      // TODO: Obsługa pliku SWZ
    }
  };

  const evaluationCriteria = [
    {
      icon: DollarSign,
      title: "Cena",
      percentage: 60,
      iconBgClass: "bg-primary/10",
      iconColorClass: "text-primary",
    },
    {
      icon: ShieldCheck,
      title: "Jakość",
      percentage: 20,
      iconBgClass: "bg-success/10",
      iconColorClass: "text-success",
    },
    {
      icon: Calendar,
      title: "Gwarancja",
      percentage: 20,
      iconBgClass: "bg-primary/10",
      iconColorClass: "text-primary",
    },
  ];

  return (
    <div className="min-h-screen bg-background">
      <Header />

      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Header Section */}
        <div className="bg-card rounded-xl border border-border p-6 mb-6 animate-fade-in">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-foreground mb-1">
                Analiza Ofert Przetargowych
              </h1>
              <p className="text-muted-foreground">
                Porównuj wyniki, analizuj oferty przetargowe i zarządzaj zgodnością.
              </p>
            </div>
            <div className="flex items-center gap-3">
              <input
                type="file"
                ref={swzFileInputRef}
                onChange={handleSwzFileUpload}
                accept=".doc,.docx,.pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/pdf"
                className="hidden"
              />
              <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button 
                      className="gap-2"
                      onClick={() => swzFileInputRef.current?.click()}
                    >
                      <FileText className="w-4 h-4" />
                      Pobierz plik SWZ
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent className="p-3">
                    <p className="font-semibold mb-1">Akceptowalne formaty:</p>
                    <ul className="text-sm space-y-1">
                      <li>• .pdf (PDF)</li>
                      <li>• .doc (Word 97-2003)</li>
                      <li>• .docx (Word)</li>
                    </ul>
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
              <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button className="gap-2">
                      <Upload className="w-4 h-4" />
                      Wgraj oferty PDF
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>Obsługiwane formaty: PDF</p>
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
            </div>
          </div>
        </div>

        {/* Evaluation Criteria Section */}
        <div className="bg-card rounded-xl border border-border p-6 mb-6 animate-fade-in" style={{ animationDelay: "0.1s" }}>
          <h2 className="text-lg font-semibold text-foreground mb-1">
            Wagi Kryteriów Oceny
          </h2>
          <p className="text-sm text-muted-foreground mb-5">
            Aktualna logika punktacji stosowana do przesłanych ofert.
          </p>

          <div className="flex flex-col sm:flex-row gap-4">
            {evaluationCriteria.map((criteria) => (
              <EvaluationCriteriaCard
                key={criteria.title}
                icon={criteria.icon}
                title={criteria.title}
                percentage={criteria.percentage}
                iconBgClass={criteria.iconBgClass}
                iconColorClass={criteria.iconColorClass}
              />
            ))}
          </div>
        </div>

        {/* Actions Bar */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-4 animate-fade-in" style={{ animationDelay: "0.2s" }}>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="icon" className="h-9 w-9">
              <SlidersHorizontal className="w-4 h-4" />
            </Button>
            <Button variant="outline" size="icon" className="h-9 w-9">
              <ArrowUpDown className="w-4 h-4" />
            </Button>
          </div>

          <div className="flex items-center gap-3">
            <Button variant="outline" className="gap-2">
              <AlertCircle className="w-4 h-4" />
              Wyjaśnienia
            </Button>
            <Button className="gap-2">
              <FileSpreadsheet className="w-4 h-4" />
              Eksport do Excel
            </Button>
          </div>
        </div>

        {/* Offers Table */}
        <OffersTable />
      </main>
    </div>
  );
};

export default OffersAnalysis;
