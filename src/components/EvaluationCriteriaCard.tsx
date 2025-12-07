import { LucideIcon } from "lucide-react";

interface EvaluationCriteriaCardProps {
  icon: LucideIcon;
  title: string;
  percentage: number;
  iconBgClass?: string;
  iconColorClass?: string;
}

const EvaluationCriteriaCard = ({
  icon: Icon,
  title,
  percentage,
  iconBgClass = "bg-primary/10",
  iconColorClass = "text-primary",
}: EvaluationCriteriaCardProps) => {
  return (
    <div className="bg-secondary/50 rounded-xl p-5 flex-1 min-w-[200px] transition-all hover:bg-secondary/70">
      <div className={`w-10 h-10 ${iconBgClass} rounded-lg flex items-center justify-center mb-3`}>
        <Icon className={`w-5 h-5 ${iconColorClass}`} />
      </div>
      <h3 className="font-semibold text-foreground mb-1">{title}</h3>
      <p className="text-sm text-muted-foreground">{percentage}% of total score</p>
    </div>
  );
};

export default EvaluationCriteriaCard;
