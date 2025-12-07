import { FileText, Save } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

export function Header() {
  return (
    <header className="h-16 border-b border-border bg-card px-4 flex items-center justify-between shadow-soft">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
          <FileText className="w-5 h-5 text-primary-foreground" />
        </div>
        <span className="font-semibold text-lg text-foreground">SWZ Generator AI</span>
      </div>
      
      <div className="flex items-center gap-3">
        <Button variant="outline" size="sm" className="gap-2">
          <Save className="w-4 h-4" />
          Zapisz
        </Button>
        
        <div className="flex items-center gap-3 ml-4 pl-4 border-l border-border">
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
