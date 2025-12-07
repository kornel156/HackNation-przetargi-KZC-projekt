import { useState, useEffect } from "react";
import { ChevronDown, Building2, FileText, Calendar, BarChart3, Shield, FileCheck, MessageSquare, Settings } from "lucide-react";
import { cn } from "@/lib/utils";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Switch } from "@/components/ui/switch";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

// Typy danych SWZ odpowiadające backendowi
export interface SWZFormData {
  // Dane zamawiającego
  organization_name: string;
  address: string;
  nip: string;
  regon: string;
  contact_email: string;
  phone: string;
  website: string;
  person_responsible: string;
  
  // Tryb i przedmiot
  procurement_mode: string;
  legal_basis: string;
  procurement_title: string;
  procurement_id: string;
  cpv_codes: string;
  procurement_type: string;
  description: string;
  
  // Terminy
  execution_deadline: string;
  variants_allowed: boolean;
  submission_deadline: string;
  opening_date: string;
  binding_period: string;
  
  // Kryteria
  criteria_price_weight: string;
  criteria_other_name: string;
  criteria_other_weight: string;
  budget: string;
  quality_features: string;
  
  // Warunki i wykluczenia
  exclusion_grounds_optional: string;
  participation_conditions: string;
  required_documents: string;
  
  // Umowa
  contract_terms: string;
  legal_protection_info: string;
  
  // Komunikacja
  communication_rules: string;
  evaluation_procedure: string;
  
  // Dodatkowe
  consortium_rules: string;
  subcontracting_rules: string;
  lots: string;
  employment_requirements: string;
  social_clauses: string;
  warranty_terms: string;
  special_requirements: string;
}

const defaultFormData: SWZFormData = {
  organization_name: "",
  address: "",
  nip: "",
  regon: "",
  contact_email: "",
  phone: "",
  website: "",
  person_responsible: "",
  procurement_mode: "",
  legal_basis: "",
  procurement_title: "",
  procurement_id: "",
  cpv_codes: "",
  procurement_type: "",
  description: "",
  execution_deadline: "",
  variants_allowed: false,
  submission_deadline: "",
  opening_date: "",
  binding_period: "",
  criteria_price_weight: "60",
  criteria_other_name: "",
  criteria_other_weight: "",
  budget: "",
  quality_features: "",
  exclusion_grounds_optional: "",
  participation_conditions: "",
  required_documents: "",
  contract_terms: "",
  legal_protection_info: "",
  communication_rules: "",
  evaluation_procedure: "",
  consortium_rules: "",
  subcontracting_rules: "",
  lots: "",
  employment_requirements: "",
  social_clauses: "",
  warranty_terms: "",
  special_requirements: "",
};

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
          isOpen ? "max-h-[800px] opacity-100" : "max-h-0 opacity-0"
        )}
      >
        <div className="px-4 pb-4 pt-2 space-y-4 border-t border-border">
          {children}
        </div>
      </div>
    </div>
  );
}

interface ParametersPanelProps {
  data?: any;
  onFormChange?: (markdownContent: string, swzData: any) => void;
}

export function ParametersPanel({ data, onFormChange }: ParametersPanelProps) {
  const [formData, setFormData] = useState<SWZFormData>(defaultFormData);
  const [isUpdating, setIsUpdating] = useState(false);

  // Synchronizuj dane z props
  useEffect(() => {
    if (data) {
      setFormData(prev => ({
        ...prev,
        organization_name: data.organization_name || "",
        address: data.address || "",
        nip: data.nip || "",
        regon: data.regon || "",
        contact_email: data.contact_email || "",
        phone: data.phone || "",
        website: data.website || "",
        person_responsible: data.person_responsible || "",
        procurement_mode: data.procurement_mode || "",
        legal_basis: data.legal_basis || "",
        procurement_title: data.procurement_title || "",
        procurement_id: data.procurement_id || "",
        cpv_codes: Array.isArray(data.cpv_codes) ? data.cpv_codes.join(", ") : "",
        procurement_type: data.procurement_type || "",
        description: data.description || "",
        execution_deadline: data.execution_deadline || "",
        variants_allowed: data.variants_allowed || false,
        submission_deadline: data.submission_deadline || "",
        opening_date: data.opening_date || "",
        binding_period: data.binding_period || "",
        budget: data.budget ? String(data.budget) : "",
        warranty_terms: data.warranty_terms || "",
        special_requirements: data.special_requirements || "",
      }));
    }
  }, [data]);

  const handleChange = (field: keyof SWZFormData, value: string | boolean) => {
    const newData = { ...formData, [field]: value };
    setFormData(newData);
  };

  const handleSubmit = async () => {
    setIsUpdating(true);
    try {
      const response = await fetch("http://localhost:8000/update-swz", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      
      if (response.ok) {
        const result = await response.json();
        if (onFormChange) {
          onFormChange(result.markdown_content, result.swz_data);
        }
      }
    } catch (error) {
      console.error("Błąd aktualizacji:", error);
    } finally {
      setIsUpdating(false);
    }
  };

  return (
    <aside className="w-80 border-r border-border bg-background p-4 flex flex-col gap-4 overflow-y-auto scrollbar-thin">
      <div className="mb-2">
        <h2 className="font-semibold text-foreground">Parametry Zamówienia</h2>
        <p className="text-sm text-muted-foreground">Wypełnij dane SWZ</p>
      </div>

      {/* SEKCJA I: DANE ZAMAWIAJĄCEGO */}
      <AccordionSection
        icon={<Building2 className="w-4 h-4" />}
        title="I. Dane Zamawiającego"
        defaultOpen={true}
      >
        <div className="space-y-3">
          <div>
            <Label htmlFor="organization_name" className="text-xs text-muted-foreground">
              Nazwa zamawiającego
            </Label>
            <Input
              id="organization_name"
              placeholder="np. Urząd Miasta Warszawa"
              value={formData.organization_name}
              onChange={(e) => handleChange("organization_name", e.target.value)}
              className="mt-1"
            />
          </div>
          <div>
            <Label htmlFor="address" className="text-xs text-muted-foreground">
              Adres
            </Label>
            <Input
              id="address"
              placeholder="np. ul. Marszałkowska 1, 00-001 Warszawa"
              value={formData.address}
              onChange={(e) => handleChange("address", e.target.value)}
              className="mt-1"
            />
          </div>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <Label htmlFor="nip" className="text-xs text-muted-foreground">
                NIP
              </Label>
              <Input
                id="nip"
                placeholder="000-000-00-00"
                value={formData.nip}
                onChange={(e) => handleChange("nip", e.target.value)}
                className="mt-1"
              />
            </div>
            <div>
              <Label htmlFor="regon" className="text-xs text-muted-foreground">
                REGON
              </Label>
              <Input
                id="regon"
                placeholder="000000000"
                value={formData.regon}
                onChange={(e) => handleChange("regon", e.target.value)}
                className="mt-1"
              />
            </div>
          </div>
          <div>
            <Label htmlFor="contact_email" className="text-xs text-muted-foreground">
              Email kontaktowy
            </Label>
            <Input
              id="contact_email"
              type="email"
              placeholder="zamowienia@urzad.pl"
              value={formData.contact_email}
              onChange={(e) => handleChange("contact_email", e.target.value)}
              className="mt-1"
            />
          </div>
          <div>
            <Label htmlFor="phone" className="text-xs text-muted-foreground">
              Telefon
            </Label>
            <Input
              id="phone"
              placeholder="+48 22 000 00 00"
              value={formData.phone}
              onChange={(e) => handleChange("phone", e.target.value)}
              className="mt-1"
            />
          </div>
          <div>
            <Label htmlFor="website" className="text-xs text-muted-foreground">
              Strona internetowa (opcjonalnie)
            </Label>
            <Input
              id="website"
              placeholder="https://www.urzad.pl"
              value={formData.website}
              onChange={(e) => handleChange("website", e.target.value)}
              className="mt-1"
            />
          </div>
          <div>
            <Label htmlFor="person_responsible" className="text-xs text-muted-foreground">
              Osoba odpowiedzialna
            </Label>
            <Input
              id="person_responsible"
              placeholder="Jan Kowalski - Kierownik Działu Zamówień"
              value={formData.person_responsible}
              onChange={(e) => handleChange("person_responsible", e.target.value)}
              className="mt-1"
            />
          </div>
        </div>
      </AccordionSection>

      {/* SEKCJA II: TRYB I PRZEDMIOT */}
      <AccordionSection
        icon={<FileText className="w-4 h-4" />}
        title="II. Tryb i Przedmiot Zamówienia"
      >
        <div className="space-y-3">
          <div>
            <Label htmlFor="procurement_mode" className="text-xs text-muted-foreground">
              Tryb postępowania
            </Label>
            <Select 
              value={formData.procurement_mode} 
              onValueChange={(v) => handleChange("procurement_mode", v)}
            >
              <SelectTrigger className="mt-1">
                <SelectValue placeholder="Wybierz tryb postępowania" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Tryb podstawowy bez negocjacji (art. 275 pkt 1 PZP)">Tryb podstawowy bez negocjacji</SelectItem>
                <SelectItem value="Tryb podstawowy z możliwością negocjacji (art. 275 pkt 2 PZP)">Tryb podstawowy z negocjacjami</SelectItem>
                <SelectItem value="Przetarg nieograniczony (art. 132 PZP)">Przetarg nieograniczony</SelectItem>
                <SelectItem value="Przetarg ograniczony (art. 134 PZP)">Przetarg ograniczony</SelectItem>
                <SelectItem value="Negocjacje z ogłoszeniem (art. 153 PZP)">Negocjacje z ogłoszeniem</SelectItem>
                <SelectItem value="Dialog konkurencyjny (art. 172 PZP)">Dialog konkurencyjny</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label htmlFor="legal_basis" className="text-xs text-muted-foreground">
              Podstawa prawna
            </Label>
            <Input
              id="legal_basis"
              placeholder="np. art. 275 pkt 1 ustawy PZP"
              value={formData.legal_basis}
              onChange={(e) => handleChange("legal_basis", e.target.value)}
              className="mt-1"
            />
          </div>
          <div>
            <Label htmlFor="procurement_title" className="text-xs text-muted-foreground">
              Nazwa zamówienia
            </Label>
            <Input
              id="procurement_title"
              placeholder="np. Budowa hali sportowej przy SP nr 5"
              value={formData.procurement_title}
              onChange={(e) => handleChange("procurement_title", e.target.value)}
              className="mt-1"
            />
          </div>
          <div>
            <Label htmlFor="procurement_id" className="text-xs text-muted-foreground">
              Numer referencyjny
            </Label>
            <Input
              id="procurement_id"
              placeholder="np. ZP.271.1.2024"
              value={formData.procurement_id}
              onChange={(e) => handleChange("procurement_id", e.target.value)}
              className="mt-1"
            />
          </div>
          <div>
            <Label htmlFor="cpv_codes" className="text-xs text-muted-foreground">
              Kody CPV (rozdzielone przecinkami)
            </Label>
            <Input
              id="cpv_codes"
              placeholder="45212225-9, 45000000-7"
              value={formData.cpv_codes}
              onChange={(e) => handleChange("cpv_codes", e.target.value)}
              className="mt-1"
            />
          </div>
          <div>
            <Label htmlFor="procurement_type" className="text-xs text-muted-foreground">
              Rodzaj zamówienia
            </Label>
            <Select 
              value={formData.procurement_type} 
              onValueChange={(v) => handleChange("procurement_type", v)}
            >
              <SelectTrigger className="mt-1">
                <SelectValue placeholder="Wybierz rodzaj" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Roboty budowlane">Roboty budowlane</SelectItem>
                <SelectItem value="Dostawy">Dostawy</SelectItem>
                <SelectItem value="Usługi">Usługi</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label htmlFor="description" className="text-xs text-muted-foreground">
              Opis przedmiotu zamówienia
            </Label>
            <Textarea
              id="description"
              placeholder="Szczegółowy opis przedmiotu zamówienia..."
              value={formData.description}
              onChange={(e) => handleChange("description", e.target.value)}
              className="mt-1 min-h-[80px]"
            />
          </div>
        </div>
      </AccordionSection>

      {/* SEKCJA III: TERMINY */}
      <AccordionSection
        icon={<Calendar className="w-4 h-4" />}
        title="III. Terminy"
      >
        <div className="space-y-3">
          <div>
            <Label htmlFor="execution_deadline" className="text-xs text-muted-foreground">
              Termin wykonania zamówienia
            </Label>
            <Input
              id="execution_deadline"
              placeholder="np. 12 miesięcy od podpisania umowy"
              value={formData.execution_deadline}
              onChange={(e) => handleChange("execution_deadline", e.target.value)}
              className="mt-1"
            />
          </div>
          <div className="flex items-center justify-between">
            <Label htmlFor="variants_allowed" className="text-xs text-muted-foreground">
              Oferty wariantowe dopuszczone
            </Label>
            <Switch
              id="variants_allowed"
              checked={formData.variants_allowed}
              onCheckedChange={(checked) => handleChange("variants_allowed", checked)}
            />
          </div>
          <div>
            <Label htmlFor="submission_deadline" className="text-xs text-muted-foreground">
              Termin składania ofert
            </Label>
            <Input
              id="submission_deadline"
              type="datetime-local"
              value={formData.submission_deadline}
              onChange={(e) => handleChange("submission_deadline", e.target.value)}
              className="mt-1"
            />
          </div>
          <div>
            <Label htmlFor="opening_date" className="text-xs text-muted-foreground">
              Termin otwarcia ofert
            </Label>
            <Input
              id="opening_date"
              type="datetime-local"
              value={formData.opening_date}
              onChange={(e) => handleChange("opening_date", e.target.value)}
              className="mt-1"
            />
          </div>
          <div>
            <Label htmlFor="binding_period" className="text-xs text-muted-foreground">
              Termin związania ofertą
            </Label>
            <Input
              id="binding_period"
              placeholder="np. 30 dni od terminu składania ofert"
              value={formData.binding_period}
              onChange={(e) => handleChange("binding_period", e.target.value)}
              className="mt-1"
            />
          </div>
        </div>
      </AccordionSection>

      {/* SEKCJA IV: KRYTERIA OCENY */}
      <AccordionSection
        icon={<BarChart3 className="w-4 h-4" />}
        title="IV. Kryteria Oceny Ofert"
      >
        <div className="space-y-3">
          <div>
            <Label className="text-xs text-muted-foreground">
              Waga kryterium ceny (%)
            </Label>
            <Input
              type="number"
              min="0"
              max="100"
              placeholder="60"
              value={formData.criteria_price_weight}
              onChange={(e) => handleChange("criteria_price_weight", e.target.value)}
              className="mt-1"
            />
          </div>
          <div>
            <Label className="text-xs text-muted-foreground">
              Drugie kryterium (nazwa)
            </Label>
            <Input
              placeholder="np. Termin realizacji"
              value={formData.criteria_other_name}
              onChange={(e) => handleChange("criteria_other_name", e.target.value)}
              className="mt-1"
            />
          </div>
          <div>
            <Label className="text-xs text-muted-foreground">
              Waga drugiego kryterium (%)
            </Label>
            <Input
              type="number"
              min="0"
              max="100"
              placeholder="40"
              value={formData.criteria_other_weight}
              onChange={(e) => handleChange("criteria_other_weight", e.target.value)}
              className="mt-1"
            />
          </div>
          <div>
            <Label htmlFor="budget" className="text-xs text-muted-foreground">
              Budżet (PLN)
            </Label>
            <Input
              id="budget"
              type="number"
              placeholder="np. 1000000"
              value={formData.budget}
              onChange={(e) => handleChange("budget", e.target.value)}
              className="mt-1"
            />
          </div>
          <div>
            <Label htmlFor="quality_features" className="text-xs text-muted-foreground">
              Cechy jakościowe (każda w nowej linii)
            </Label>
            <Textarea
              id="quality_features"
              placeholder="np.&#10;Materiały klasy A&#10;Certyfikat ISO&#10;Doświadczenie min. 5 lat"
              value={formData.quality_features}
              onChange={(e) => handleChange("quality_features", e.target.value)}
              className="mt-1 min-h-[60px]"
            />
          </div>
        </div>
      </AccordionSection>

      {/* SEKCJA V: WARUNKI I WYKLUCZENIA */}
      <AccordionSection
        icon={<Shield className="w-4 h-4" />}
        title="V. Warunki i Wykluczenia"
      >
        <div className="space-y-3">
          <div>
            <Label className="text-xs text-muted-foreground">
              Fakultatywne podstawy wykluczenia
            </Label>
            <Textarea
              placeholder="np.&#10;art. 109 ust. 1 pkt 1&#10;art. 109 ust. 1 pkt 4"
              value={formData.exclusion_grounds_optional}
              onChange={(e) => handleChange("exclusion_grounds_optional", e.target.value)}
              className="mt-1 min-h-[60px]"
            />
          </div>
          <div>
            <Label className="text-xs text-muted-foreground">
              Warunki udziału w postępowaniu
            </Label>
            <Textarea
              placeholder="np.&#10;Doświadczenie w realizacji podobnych zamówień&#10;Potencjał techniczny"
              value={formData.participation_conditions}
              onChange={(e) => handleChange("participation_conditions", e.target.value)}
              className="mt-1 min-h-[60px]"
            />
          </div>
          <div>
            <Label className="text-xs text-muted-foreground">
              Wymagane dokumenty
            </Label>
            <Textarea
              placeholder="np.&#10;Wykaz zrealizowanych zamówień&#10;Polisa OC&#10;Zaświadczenie ZUS"
              value={formData.required_documents}
              onChange={(e) => handleChange("required_documents", e.target.value)}
              className="mt-1 min-h-[60px]"
            />
          </div>
        </div>
      </AccordionSection>

      {/* SEKCJA VI: UMOWA */}
      <AccordionSection
        icon={<FileCheck className="w-4 h-4" />}
        title="VI. Warunki Umowy"
      >
        <div className="space-y-3">
          <div>
            <Label className="text-xs text-muted-foreground">
              Istotne postanowienia umowy
            </Label>
            <Textarea
              placeholder="np.&#10;Kary umowne za opóźnienia&#10;Warunki płatności&#10;Gwarancja należytego wykonania"
              value={formData.contract_terms}
              onChange={(e) => handleChange("contract_terms", e.target.value)}
              className="mt-1 min-h-[60px]"
            />
          </div>
          <div>
            <Label className="text-xs text-muted-foreground">
              Informacje o środkach ochrony prawnej
            </Label>
            <Textarea
              placeholder="Informacje o odwołaniach do KIO..."
              value={formData.legal_protection_info}
              onChange={(e) => handleChange("legal_protection_info", e.target.value)}
              className="mt-1 min-h-[60px]"
            />
          </div>
        </div>
      </AccordionSection>

      {/* SEKCJA VII: KOMUNIKACJA */}
      <AccordionSection
        icon={<MessageSquare className="w-4 h-4" />}
        title="VII. Komunikacja i Procedura"
      >
        <div className="space-y-3">
          <div>
            <Label className="text-xs text-muted-foreground">
              Zasady komunikacji
            </Label>
            <Textarea
              placeholder="np. Komunikacja za pośrednictwem platformy e-Zamówienia..."
              value={formData.communication_rules}
              onChange={(e) => handleChange("communication_rules", e.target.value)}
              className="mt-1 min-h-[60px]"
            />
          </div>
          <div>
            <Label className="text-xs text-muted-foreground">
              Procedura oceny ofert
            </Label>
            <Textarea
              placeholder="Opis procedury oceny i wyboru najkorzystniejszej oferty..."
              value={formData.evaluation_procedure}
              onChange={(e) => handleChange("evaluation_procedure", e.target.value)}
              className="mt-1 min-h-[60px]"
            />
          </div>
        </div>
      </AccordionSection>

      {/* SEKCJA VIII: DODATKOWE WYMAGANIA */}
      <AccordionSection
        icon={<Settings className="w-4 h-4" />}
        title="VIII. Dodatkowe Wymagania"
      >
        <div className="space-y-3">
          <div>
            <Label className="text-xs text-muted-foreground">
              Zasady dla konsorcjów
            </Label>
            <Textarea
              placeholder="Warunki wspólnego ubiegania się o zamówienie..."
              value={formData.consortium_rules}
              onChange={(e) => handleChange("consortium_rules", e.target.value)}
              className="mt-1 min-h-[50px]"
            />
          </div>
          <div>
            <Label className="text-xs text-muted-foreground">
              Zasady podwykonawstwa
            </Label>
            <Textarea
              placeholder="Wymagania dotyczące podwykonawców..."
              value={formData.subcontracting_rules}
              onChange={(e) => handleChange("subcontracting_rules", e.target.value)}
              className="mt-1 min-h-[50px]"
            />
          </div>
          <div>
            <Label className="text-xs text-muted-foreground">
              Części zamówienia (każda w nowej linii)
            </Label>
            <Textarea
              placeholder="np.&#10;Część 1: Roboty budowlane&#10;Część 2: Wyposażenie"
              value={formData.lots}
              onChange={(e) => handleChange("lots", e.target.value)}
              className="mt-1 min-h-[50px]"
            />
          </div>
          <div>
            <Label className="text-xs text-muted-foreground">
              Wymagania dot. zatrudnienia
            </Label>
            <Input
              placeholder="np. Zatrudnienie na umowę o pracę"
              value={formData.employment_requirements}
              onChange={(e) => handleChange("employment_requirements", e.target.value)}
              className="mt-1"
            />
          </div>
          <div>
            <Label className="text-xs text-muted-foreground">
              Klauzule społeczne
            </Label>
            <Input
              placeholder="np. Zatrudnienie osób niepełnosprawnych"
              value={formData.social_clauses}
              onChange={(e) => handleChange("social_clauses", e.target.value)}
              className="mt-1"
            />
          </div>
          <div>
            <Label className="text-xs text-muted-foreground">
              Warunki gwarancji
            </Label>
            <Input
              placeholder="np. 36 miesięcy gwarancji"
              value={formData.warranty_terms}
              onChange={(e) => handleChange("warranty_terms", e.target.value)}
              className="mt-1"
            />
          </div>
          <div>
            <Label className="text-xs text-muted-foreground">
              Wymagania specjalne
            </Label>
            <Textarea
              placeholder="Inne specjalne wymagania..."
              value={formData.special_requirements}
              onChange={(e) => handleChange("special_requirements", e.target.value)}
              className="mt-1 min-h-[50px]"
            />
          </div>
        </div>
      </AccordionSection>

      {/* PRZYCISK AKTUALIZACJI */}
      <Button 
        onClick={handleSubmit} 
        disabled={isUpdating}
        className="w-full mt-2"
      >
        {isUpdating ? "Aktualizowanie..." : "Aktualizuj dokument SWZ"}
      </Button>
    </aside>
  );
}
