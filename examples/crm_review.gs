/**
 * Public GAS sample. Run only with a sheet you create for this demo.
 * No OCR, external API, production spreadsheet ID, or customer data is used.
 */
function registerReviewedCard(sheet, card) {
  if (!card.reviewed) throw new Error('人による確認が必要です');
  const company = String(card.company || '').trim();
  const person = String(card.person || '').trim();
  if (!company || !person) throw new Error('会社名と担当者名を確認してください');

  const normalized = value => String(value).normalize('NFKC').replace(/\s+/g, '').toLowerCase();
  const key = normalized(company) + '|' + normalized(person);
  const rows = sheet.getDataRange().getValues();
  const duplicate = rows.slice(1).some(row =>
    normalized(row[0]) + '|' + normalized(row[1]) === key
  );
  if (duplicate) return { status: 'duplicate', key };

  sheet.appendRow([company, person, new Date(), '確認済み']);
  return { status: 'registered', key };
}
