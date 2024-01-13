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

export const MaxWidthUseScreen = styled.View`
  width: 90%;
  margin: 0 auto;

  @media ${devices.tablet} {
    width: 70%;
  }
`;

export const FiltersContainer = styled.View`
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  gap: 5px;
  margin-top: 10px;
  margin-right: 10px;
`;

export const CardsContainer = styled.View`
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  flex-direction: row;
  margin: 20px;
`;
