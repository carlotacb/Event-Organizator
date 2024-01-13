import React from "react";

export const handleOnChange = (
  text: string,
  input: string,
  setInputs: React.Dispatch<React.SetStateAction<any>>,
) => {
  // @ts-ignore
  setInputs((prevState) => ({ ...prevState, [input]: text }));
};

export const handleError = (
  text: string | undefined,
  input: string,
  setErrors: React.Dispatch<React.SetStateAction<any>>,
) => {
  // @ts-ignore
  setErrors((prevState) => ({ ...prevState, [input]: text }));
};
