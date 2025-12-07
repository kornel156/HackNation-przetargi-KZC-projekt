import { FileText, BarChart3, ClipboardList } from "lucide-react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Link, useLocation } from "react-router-dom";

interface HeaderProps {
  currentPage?: "swz" | "offers" | "protocol";
}

export function Header({ currentPage }: HeaderProps) {
  const location = useLocation();
  const path = location.pathname;
  
  // Określ aktualną stronę na podstawie ścieżki
  const activePage = currentPage || (
    path === "/analiza-ofert" ? "offers" :
    path === "/protokol" ? "protocol" : "swz"
  );

  const getTitle = () => {
    switch (activePage) {
      case "offers": return "Analiza Ofert Przetargowych";
      case "protocol": return "Generator Protokołu Przetargu";
      default: return "SWZ Generator AI";
    }
  };

  return (
    <header className="h-16 border-b border-border bg-card px-4 flex items-center justify-between shadow-soft">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
          <FileText className="w-5 h-5 text-primary-foreground" />
        </div>
        <span className="font-semibold text-lg text-foreground">{getTitle()}</span>
      </div>
      
      <div className="flex items-center gap-2">
        {/* Nawigacja między stronami */}
        {activePage !== "swz" && (
          <Link to="/">
            <Button variant="ghost" size="sm" className="gap-2">
              <FileText className="w-4 h-4" />
              Generator SWZ
            </Button>
          </Link>
        )}
        {activePage !== "offers" && (
          <Link to="/analiza-ofert">
            <Button variant="ghost" size="sm" className="gap-2">
              <BarChart3 className="w-4 h-4" />
              Analiza Ofert
            </Button>
          </Link>
        )}
        {activePage !== "protocol" && (
          <Link to="/protokol">
            <Button variant="ghost" size="sm" className="gap-2">
              <ClipboardList className="w-4 h-4" />
              Protokół Przetargu
            </Button>
          </Link>
        )}
        
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
  );
}
