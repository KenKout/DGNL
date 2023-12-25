# Vulnerability Report for [Thi Năng Lực - DGNL VNUHCM]

## Overview

This document outlines the discovery and responsible disclosure of a security vulnerability in the [Thi Năng Lực - DGNL VNUHCM]. The vulnerability allowed unauthorized access to sensitive user information.

## Vulnerability Details

### Description

The vulnerability was identified as a result of a flaw in the [Thi Năng Lực - DGNL VNUHCM] system, allowing users to access the personal data of other participants. The issue involved a lack of proper authorization checks, enabling unintended access to confidential information.

### Exploitation Method

The vulnerability could be exploited by sending a POST request to the following URL:

```
https://thinangluc.vnuhcm.edu.vn/dgnl/api-dgnl/app/tra-cuu-thong-tin-ho-so/v1?tuychon=KETQUATHI
```

The POST data included a specific identifier (`maHoSoXetTuyen`), which could be sequentially enumerated to access different user profiles.

### Raw JSON Data

```json
{
  "code": "0",
  "msg": "done",
  "data": [
    {
      "cmndSo": "079205xxxxxx",
      "maHoSoXetTuyen": "D23xxxxxx",
      "capNhat": "03/04/2023 00:00:00",
      "noiDung": "<b>THÔNG TIN THÍ SINH </b> <br/>  Họ và tên: <b>NGUYỄN XX XX LONG</b><br/> Ngày sinh: xx/xx/2005 <br/> Email: xx@gmail.com <br/> Địa chỉ: XX - XX <br/><br/> <b>THÔNG TIN DỰ THI  </b> <br/>Số báo danh: XX <br/> Ngày giờ thi: 7g30 ngày 26/3/2023 <br/>Địa điểm thi: Trường ĐH Công nghệ Thông tin, Khu phố 6, Phường Linh Trung, TP.Thủ Đức, TP.HCM<br/> Phòng thi: P.048 [B7.08.2]<br/>  <br/> <b>KẾT QUẢ THI</b><span style='color: green;'><ul><li>Tiếng Việt: 177 điểm.</li><li>Tiếng Anh: 176 điểm.</li><li>Toán-Logic-Phân tích số liệu: 231 điểm.</li><li>Khoa học Tự nhiên: 148 điểm.</li><li>Khoa học Xã hội: 129 điểm.</li></ul></span><ul><b style=color:red;'>Tổng: 861 điểm.</b></ul>"
    }
  ],
  "sign": ""
}
```
### Data Exposed

The exposed data included:

- National Identification Number (Căn Cước Công Dân)
- Name
- Date of Birth
- Email
- Address
- Exam Results
  
Over 130,000 data entries were potentially exposed due to this vulnerability.

## Responsible Disclosure

The vulnerability was responsibly disclosed to Vietnam National University, Ho Chi Minh City on June 29, 2023. Subsequent to the disclosure, the issue was addressed and fixed on July 30, 2023.

## Communication with Vietnam National University, Ho Chi Minh City

The communication with Vietnam National University, Ho Chi Minh City regarding the vulnerability was initiated on July 19, 2023. The University acknowledged the issue and subsequently resolved it.

![Communication with Vietnam National University, Ho Chi Minh City](https://github.com/KenKout/DGNL/assets/54569460/e6fc2821-be32-40c1-8c89-b252c1adc38d)

## Resolution Timeline

- **Discovery Date:** June 12, 2023
- **Disclosure Date:** June 29, 2023
- **Fix Date:** July 30, 2023

## Acknowledgment

While the vulnerability was reported in good faith with the intent of enhancing system security, no acknowledgment, certificate, or bounty was provided by Vietnam National University, Ho Chi Minh City.

## Script Details

The script sends POST requests to the vulnerable API endpoint, sequentially iterating through a range of identifiers (`maHoSoXetTuyen`). The retrieved data is then written to a file (`output.txt`), and the script displays the Count Per Minute (CPM) indicating the rate of successful requests.

### Configuration

Adjust the script's configuration variables as needed:

- `current`: Starting identifier (e.g., `100000`)
- `max_threads`: Maximum number of concurrent threads
- `max_retries`: Maximum number of retry attempts for failed requests
- `chunk_size`: Number of identifiers to process in each batch

## Disclaimer

The provided information is for educational purposes only. The intention is to raise awareness about security issues and promote responsible disclosure.
