interface SimilarityMeterProps {
  similarity: number;
}

export function SimilarityMeter({ similarity }: SimilarityMeterProps) {
  // Convert similarity to percentage
  const percentage = Math.round(similarity * 100);

  // Determine color based on similarity
  const getColor = () => {
    if (percentage >= 90) return "bg-green-500";
    if (percentage >= 80) return "bg-green-400";
    if (percentage >= 70) return "bg-yellow-400";
    if (percentage >= 60) return "bg-yellow-500";
    if (percentage >= 50) return "bg-orange-500";
    return "bg-red-500";
  };

  return (
    <div className="w-full">
      <div className="flex justify-between text-xs mb-1">
        <span className="text-gray-400">Match</span>
        <span className="font-medium">{percentage}%</span>
      </div>
      <div className="h-2 w-full bg-gray-700 rounded-full overflow-hidden">
        <div
          className={`h-full ${getColor()} transition-all duration-500 ease-out`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
