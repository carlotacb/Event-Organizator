import { Text } from "react-native";
// @ts-ignore
import styled from "styled-components/native";
import { systemColors } from "../tokens";

export const Title = styled(Text)`
  font-size: 30px;
  font-weight: bold;
  color: black;
  text-align: center;
`;

export const SubTitle = styled(Text)`
  font-size: 16px;
  color: gray;
  margin: 10px 0 30px 0;
  text-align: center;
`;

export const Description = styled(Text)`
  font-size: 18px;
  color: gray;
  margin-top: 10px;
  font-style: italic;
`;

export const SubTitleBasic = styled(Text)`
  font-size: 22px;
  color: gray;
  font-weight: bold;
  margin: 30px 0 5px 0;
`;

export const TextLinePlain = styled.View`
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 10px;
  align-items: center;
  margin-bottom: 20px;
`;

export const FirstHeader = styled(Text)`
  font-size: 24px;
  color: ${systemColors.subtitleColor};
  font-weight: bold;
  text-align: center;
  margin: 40px 0 20px;
`;

export const TextLineText = styled(Text)`
  font-size: 18px;
  color: black;
`;

export const TextLineTextBold = styled(Text)`
  font-size: 18px;
  color: black;
`;

export const TextWithoutSpaces = styled.View``;
