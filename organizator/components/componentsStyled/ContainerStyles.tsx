// @ts-ignore
import styled from "styled-components/native";

export const BottomScreenContainer = styled.View`
  padding-top: 20px;
  padding-bottom: 20px;
  align-items: center;
  display: flex;
  box-shadow: 0 -4px 10px rgba(0, 0, 0, 0.25);
`;

export const ButtonsRowContainer = styled.View<{ marginTop?: string }>`
  display: flex;
  flex-direction: row;
  justify-content: center;
  flex-wrap: wrap;
  gap: 20px;
  margin-top: ${(props: { marginTop?: string }) => props.marginTop || "0px"};
`;
