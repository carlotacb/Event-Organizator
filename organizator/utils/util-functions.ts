export function parseDate(dateAsString: string) {
  const date = new Date(dateAsString);
  return `${date.getDate().toString().padStart(2, "0")}-${date
    .getMonth()
    .toString()
    .padStart(2, "0")}-${date.getFullYear()} at ${date
    .getHours()
    .toString()
    .padStart(2, "0")}:${date.getMinutes().toString().padStart(2, "0")} h`;
}

export function dateToPlainString(date: Date) {
  return `${date.getDate().toString().padStart(2, "0")}/${(date.getMonth() + 1)
    .toString()
    .padStart(2, "0")}/${date.getFullYear()} ${date
    .getHours()
    .toString()
    .padStart(2, "0")}:${date.getMinutes().toString().padStart(2, "0")}`;
}

export function checkDate(dateAsString: string): {
  valid: boolean;
  error: string;
} {
  const regex = /^(\d{2}\/\d{2}\/\d{4} \d{2}:\d{2})$/;

  if (regex.test(dateAsString)) {
    const { day, month, year, hours, minutes } = separateDate(dateAsString);

    if (day < 1 || day > 31) {
      return { valid: false, error: "Invalid day. Please enter a valid day." };
    }
    if (month < 0 || month > 11) {
      return {
        valid: false,
        error: "Invalid month. Please enter a valid month.",
      };
    }

    const parsedDate = new Date(year, month, day, hours, minutes);

    if (!Number.isNaN(parsedDate.getTime())) {
      return { valid: true, error: "" };
    }

    return {
      valid: false,
      error: "Invalid datetime. Please enter a valid datetime.",
    };
  }

  return {
    valid: false,
    error: "Invalid datetime format. Please enter DD/MM/YYYY HH:MM.",
  };
}

export function checkDateRange(
  startDate: string,
  endDate: string,
): { valid: boolean; error: string } {
  const startDateObject = new Date(startDate);
  const endDateObject = new Date(endDate);

  if (startDateObject.getTime() > endDateObject.getTime()) {
    return {
      valid: false,
      error: `The date should be after ${startDate}`,
    };
  }

  return { valid: true, error: "" };
}

function separateDate(dateToSeparate: string): {
  day: number;
  month: number;
  year: number;
  hours: number;
  minutes: number;
} {
  const [datePart, timePart] = dateToSeparate.split(" ");
  const [dayString, monthString, yearString] = datePart.split("/");
  const [hoursString, minutesString] = timePart.split(":");

  const day = parseInt(dayString, 10);
  const month = parseInt(monthString, 10) - 1;
  const year = parseInt(yearString, 10);
  const hours = parseInt(hoursString, 10);
  const minutes = parseInt(minutesString, 10);

  return {
    day,
    month,
    year,
    hours,
    minutes,
  };
}

export function checkURL(url: string): { valid: boolean; error: string } {
  try {
    const newURL = new URL(url);
    return { valid: true, error: `The ${newURL} is valid` };
  } catch {
    return { valid: false, error: "Invalid URL. Please enter a valid URL." };
  }
}
