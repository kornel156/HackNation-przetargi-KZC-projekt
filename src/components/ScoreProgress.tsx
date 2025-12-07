interface ScoreProgressProps {
  score: number;
}

const getScoreColor = (score: number): string => {
  if (score >= 90) return "bg-success";
  if (score >= 80) return "bg-primary";
  if (score >= 70) return "bg-warning";
  return "bg-destructive";
};

const ScoreProgress = ({ score }: ScoreProgressProps) => {
  return (
    <div className="flex items-center gap-3">
      <div className="w-24 h-2 bg-secondary rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-500 ${getScoreColor(score)}`}
          style={{ width: `${score}%` }}
        />
      </div>
      <span className="text-sm font-medium text-foreground w-10">{score}%</span>
    </div>
  );
};

export default ScoreProgress;
