import { Upload, FileSpreadsheet, AlertCircle, DollarSign, ShieldCheck, Calendar, SlidersHorizontal, ArrowUpDown, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
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
      {/* Header - taki sam styl jak na stronie generatora SWZ */}
      <header className="h-16 border-b border-border bg-card px-4 flex items-center justify-between shadow-soft">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
            <FileText className="w-5 h-5 text-primary-foreground" />
          </div>
          <span className="font-semibold text-lg text-foreground">Analiza Ofert Przetargowych</span>
        </div>
        
        <div className="flex items-center gap-3">
          <Link to="/">
            <Button variant="outline" size="sm" className="gap-2">
              <FileText className="w-4 h-4" />
              Generator SWZ
            </Button>
          </Link>
          <div className="flex items-center gap-3 pl-4 border-l border-border">
            <div className="text-right">
              <p className="text-sm font-medium text-foreground">Jan Kowalski</p>
              <p className="text-xs text-muted-foreground">Urząd Miejski</p>
            </div>
            <Avatar className="h-9 w-9">
              <AvatarImage src="https://api.dicebear.com/7.x/avataaars/svg?seed=Jan" />
              <AvatarFallback>JK</AvatarFallback>
            </Avatar>
          </div>
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
