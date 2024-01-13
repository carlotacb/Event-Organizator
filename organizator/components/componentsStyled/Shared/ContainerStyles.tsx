// @ts-ignore
import styled from "styled-components/native";
import { devices } from "../tokens";

export const BottomScreenContainer = styled.View`
  padding-top: 20px;
  padding-bottom: 20px;
  align-items: center;
  display: flex;
`;

export const ButtonsRowContainer = styled.View<{ marginTop?: string }>`
  display: flex;
  flex-direction: row;
  justify-content: center;
  flex-wrap: wrap;
  gap: 20px;
  margin-top: ${(props: { marginTop?: string }) => props.marginTop || "0px"};
`;

export const ButtonsRowContainerLeft = styled.View`
  display: flex;
  flex-direction: row;
  align-items: center;
  align-content: center;
  justify-content: flex-end;
  gap: 15px;
  margin-bottom: 25px;
`;

export const ButtonsColumnContainer = styled.View<{ marginTop?: string }>`
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 20px;
  margin-top: ${(props: { marginTop?: string }) => props.marginTop || "0px"};
`;

export const MaxWidthUseScreen = styled.View`
  width: 90%;
  margin: 0 auto;

  @media ${devices.tablet} {
    width: 70%;
  }
`;

export const MaxWidthUseScreenForList = styled.View`
  width: 100%;

  @media ${devices.tablet} {
    width: 60%;
    margin: 0 auto;
  }
`;

export const FiltersContainer = styled.View`
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  gap: 5px;
  margin-right: 10px;
`;

export const RadioButtonContainer = styled.View<{ withoutMargin: boolean }>`
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  justify-content: flex-start;
  margin-bottom: ${(props: { withoutMargin: boolean }) =>
    props.withoutMargin ? "0px" : "20px"};
`;

export const CardsContainer = styled.View`
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  flex-direction: row;
  margin: 20px;
`;
