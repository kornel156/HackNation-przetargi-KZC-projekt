import { Upload, FileSpreadsheet, AlertCircle, DollarSign, ShieldCheck, Calendar, SlidersHorizontal, ArrowUpDown, Home } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import EvaluationCriteriaCard from "@/components/EvaluationCriteriaCard";
import OffersTable from "@/components/OffersTable";

const OffersAnalysis = () => {
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
      {/* Navigation Header */}
      <header className="bg-card border-b border-border px-6 py-3">
        <div className="flex items-center justify-between max-w-7xl mx-auto">
          <div className="flex items-center gap-4">
            <Link to="/">
              <Button variant="ghost" size="sm" className="gap-2">
                <Home className="w-4 h-4" />
                Powrót do generatora SWZ
              </Button>
            </Link>
          </div>
          <span className="font-semibold text-foreground">Analiza Ofert Przetargowych</span>
        </div>
      </header>

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
              <span className="text-sm text-muted-foreground hidden sm:block">
                Obsługiwane formaty: PDF
              </span>
              <Button className="gap-2">
                <Upload className="w-4 h-4" />
                Wgraj oferty PDF
              </Button>
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
