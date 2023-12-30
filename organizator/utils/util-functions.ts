export default function parseDate(dateAsString: string) {
  const date = new Date(dateAsString);
  return `${date.getDate().toString().padStart(2, "0")}-${date
    .getMonth()
    .toString()
    .padStart(2, "0")}-${date.getFullYear()} at ${date
    .getHours()
    .toString()
    .padStart(2, "0")}:${date.getMinutes().toString().padStart(2, "0")} h`;
}
