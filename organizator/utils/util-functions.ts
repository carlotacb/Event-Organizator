import { UserRoles } from "./interfaces/Users";

export function formatDate(inputDate: string): string {
  const date = new Date(inputDate);

  const day = String(date.getDate()).padStart(2, "0");
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const year = String(date.getFullYear());
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");

  return `${day}/${month}/${year} ${hours}:${minutes}`;
}

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

export function checkDateWithTime(dateAsString: string): {
  valid: boolean;
  error: string;
} {
  const regex = /^(\d{2}\/\d{2}\/\d{4} \d{2}:\d{2})$/;

  if (regex.test(dateAsString)) {
    const { day, month, year, hours, minutes } =
      separateDateWithTime(dateAsString);

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

export function checkDateBirth(dateAsString: string): {
  valid: boolean;
  error: string;
} {
  const regex = /^(\d{2}\/\d{2}\/\d{4})$/;

  if (regex.test(dateAsString)) {
    const { day, month, year } = separateDate(dateAsString);
    const maxYear = new Date().getFullYear() - 12;

    if (day < 1 || day > 31) {
      return { valid: false, error: "Invalid day. Please enter a valid day." };
    }
    if (month < 0 || month > 11) {
      return {
        valid: false,
        error: "Invalid month. Please enter a valid month.",
      };
    }
    if (year > maxYear) {
      return {
        valid: false,
        error: `Invalid year. The maximum year is ${maxYear}`,
      };
    }

    const parsedDate = new Date(year, month, day);

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
    error: "Invalid datetime format. Please enter DD/MM/YYYY.",
  };
}

export function checkDateGraduation(dateAsString: string): {
  valid: boolean;
  error: string;
} {
  const regex = /^(\d{2}\/\d{2}\/\d{4})$/;

  if (regex.test(dateAsString)) {
    const { day, month, year } = separateDate(dateAsString);
    const thisYear = new Date().getFullYear();

    if (day < 1 || day > 31) {
      return { valid: false, error: "Invalid day. Please enter a valid day." };
    }
    if (month < 0 || month > 11) {
      return {
        valid: false,
        error: "Invalid month. Please enter a valid month.",
      };
    }
    if (year < thisYear) {
      return {
        valid: false,
        error: `Invalid year. The minimum year is ${thisYear}`,
      };
    }

    const parsedDate = new Date(year, month, day);

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
    error: "Invalid datetime format. Please enter DD/MM/YYYY.",
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

function separateDateWithTime(dateToSeparate: string): {
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

function separateDate(dateToSeparate: string): {
  day: number;
  month: number;
  year: number;
} {
  const [dayString, monthString, yearString] = dateToSeparate.split("/");

  const day = parseInt(dayString, 10);
  const month = parseInt(monthString, 10) - 1;
  const year = parseInt(yearString, 10);

  return {
    day,
    month,
    year,
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

export function getColorForApplicationStatus(st: string): string {
  if (st === "Under review") return "#f8d280";
  if (st === "Invited") return "#74b3fc";
  if (st === "Rejected") return "#ff7f7f";
  if (st === "Cancelled") return "#d33737";
  if (st === "Confirmed") return "#6cd27b";
  if (st === "Invalid") return "#867f7f";
  if (st === "Wait list") return "#b694f5";
  if (st === "Attended") return "#9df5ae";

  return "#000000";
}

export function getBackGroundColorForRole(role: string): string {
  switch (role) {
    case UserRoles.ORGANIZER_ADMIN:
      return "#cea6aa";
    case UserRoles.ORGANIZER:
      return "#aba6ce";
    default:
      return "#a6cea6";
  }
}

export const parseRole = (role: string): string => {
  switch (role) {
    case UserRoles.ORGANIZER_ADMIN:
      return "ADMIN";
    case UserRoles.ORGANIZER:
      return "Organizer";
    default:
      return "User";
  }
};

export const parseDegreeStatus = (status: string): string => {
  switch (status) {
    case "study":
      return "Studying";
    case "work":
      return "Working";
    default:
      return "Another thing";
  }
};

export const parseGender = (gender: string): string => {
  switch (gender) {
    case "FEMALE":
      return "Female";
    case "MALE":
      return "Male";
    case "NO_BINARY":
      return "Non binary";
    case "PREFER_NOT_TO_SAY":
      return "Won't say";
    default:
      return "Other";
  }
};

export const parseDiet = (diet: string): string => {
  switch (diet) {
    case "VEGAN":
      return "Vegan";
    case "VEGETARIAN":
      return "Vegetarian";
    case "GLUTEN_FREE":
      return "Gluten free";
    case "OTHER":
      return "Other";
    default:
      return "Nothing";
  }
};
