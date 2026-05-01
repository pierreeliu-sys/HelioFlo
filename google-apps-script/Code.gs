// HelioFlo — Contact Form Handler
// Deploy as: Web app → Execute as "Me" → Who has access "Anyone"

const SPREADSHEET_ID = '1Ar3i51PNrqQokQGsvLDl-SvTCEp8nt5k0Bx9zHxArRI';
const DRIVE_FOLDER   = 'HelioFlo – Site Photos';

const HEADERS = [
  'Timestamp', 'First Name', 'Last Name', 'Email', 'Phone',
  'Address', 'Property Type', 'Interest', 'Build Type',
  'Electricity Bill', 'Install Timeframe', 'Message', 'Photos'
];

function doPost(e) {
  try {
    const data  = JSON.parse(e.postData.contents);
    const sheet = SpreadsheetApp.openById(SPREADSHEET_ID).getActiveSheet();

    if (sheet.getLastRow() === 0) sheet.appendRow(HEADERS);

    const photoLinks = [];
    if (Array.isArray(data.photos) && data.photos.length) {
      const folder = getFolder(DRIVE_FOLDER);
      data.photos.forEach(p => {
        const blob = Utilities.newBlob(Utilities.base64Decode(p.data), p.type, p.name);
        const file = folder.createFile(blob);
        file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
        photoLinks.push(p.label + ': ' + file.getUrl());
      });
    }

    sheet.appendRow([
      data.timestamp        || new Date().toLocaleString('en-AU'),
      data.first_name       || '',
      data.last_name        || '',
      data.email            || '',
      data.phone            || '',
      data.address          || '',
      data.property         || '',
      data.interest         || '',
      data.build_type       || '',
      data.electricity_bill || '',
      data.install_period   || '',
      data.message          || '',
      photoLinks.join('\n'),
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ ok: false, error: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function getFolder(name) {
  const it = DriveApp.getFoldersByName(name);
  return it.hasNext() ? it.next() : DriveApp.createFolder(name);
}

function doGet() {
  return ContentService.createTextOutput('HelioFlo form endpoint is active.');
}
