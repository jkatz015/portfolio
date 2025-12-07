' ============================================================
' AP INVOICE ANOMALY DETECTOR
' Professional Excel Tool for AP/GL Operations
' ============================================================

Sub RunAnomalyDetection()
    
    Dim ws As Worksheet
    Dim lastRow As Long, lastCol As Long
    Dim i As Long
    Dim vendorId As String, amount As Double, invoiceDate As Date
    Dim flagDup As Integer, flagRound As Integer, flagWeekend As Integer
    Dim score As Integer, risk As String
    Dim dupDict As Object
    Dim key As String
    Dim startTime As Double
    
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    startTime = Timer
    
    Set ws = ThisWorkbook.Worksheets("AP_Transactions")
    Set dupDict = CreateObject("Scripting.Dictionary")
    
    lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row
    lastCol = ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column
    
    ' Add header columns
    ws.Cells(1, lastCol + 1).Value = "FLAG_DUPLICATE"
    ws.Cells(1, lastCol + 2).Value = "FLAG_ROUND_AMT"
    ws.Cells(1, lastCol + 3).Value = "FLAG_WEEKEND"
    ws.Cells(1, lastCol + 4).Value = "ANOMALY_SCORE"
    ws.Cells(1, lastCol + 5).Value = "RISK_LEVEL"
    
    ' Format headers
    With ws.Range(ws.Cells(1, lastCol + 1), ws.Cells(1, lastCol + 5))
        .Font.Bold = True
        .Interior.Color = RGB(0, 102, 204)
        .Font.Color = RGB(255, 255, 255)
    End With
    
    ' Build duplicate detection dictionary (Vendor + Amount)
    For i = 2 To lastRow
        vendorId = CStr(ws.Cells(i, 2).Value)
        amount = Round(ws.Cells(i, 9).Value, 2)
        key = vendorId & "|" & CStr(amount)
        If dupDict.exists(key) Then
            dupDict(key) = dupDict(key) + 1
        Else
            dupDict.Add key, 1
        End If
    Next i
    
    ' Process each row
    For i = 2 To lastRow
        
        vendorId = CStr(ws.Cells(i, 2).Value)
        amount = ws.Cells(i, 9).Value
        
        If IsDate(ws.Cells(i, 7).Value) Then
            invoiceDate = ws.Cells(i, 7).Value
        Else
            invoiceDate = 0
        End If
        
        flagDup = 0
        flagRound = 0
        flagWeekend = 0
        
        ' Rule 1: Duplicate Detection
        key = vendorId & "|" & CStr(Round(amount, 2))
        If dupDict.exists(key) Then
            If dupDict(key) > 1 Then flagDup = 1
        End If
        
        ' Rule 2: Round Number Detection
        If amount >= 1000 And amount = Int(amount) And (amount Mod 1000) = 0 Then
            flagRound = 1
        End If
        
        ' Rule 3: Weekend Detection
        If invoiceDate > 0 Then
            If Weekday(invoiceDate, vbSunday) = 1 Or Weekday(invoiceDate, vbSunday) = 7 Then
                flagWeekend = 1
            End If
        End If
        
        ' Calculate Score
        score = (flagDup * 3) + (flagRound * 1) + (flagWeekend * 2)
        
        ' Determine Risk Level
        If score >= 5 Then
            risk = "HIGH"
        ElseIf score >= 3 Then
            risk = "MEDIUM"
        ElseIf score >= 1 Then
            risk = "LOW"
        Else
            risk = "CLEAN"
        End If
        
        ' Write results
        ws.Cells(i, lastCol + 1).Value = flagDup
        ws.Cells(i, lastCol + 2).Value = flagRound
        ws.Cells(i, lastCol + 3).Value = flagWeekend
        ws.Cells(i, lastCol + 4).Value = score
        ws.Cells(i, lastCol + 5).Value = risk
        
        ' Color code risk level
        Select Case risk
            Case "HIGH"
                ws.Cells(i, lastCol + 5).Interior.Color = RGB(255, 0, 0)
                ws.Cells(i, lastCol + 5).Font.Color = RGB(255, 255, 255)
            Case "MEDIUM"
                ws.Cells(i, lastCol + 5).Interior.Color = RGB(255, 192, 0)
            Case "LOW"
                ws.Cells(i, lastCol + 5).Interior.Color = RGB(255, 255, 0)
            Case "CLEAN"
                ws.Cells(i, lastCol + 5).Interior.Color = RGB(146, 208, 80)
        End Select
        
    Next i
    
    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True
    
    ' Create Summary Dashboard
    Call CreateDashboard(lastRow - 1)
    
    MsgBox "Anomaly Detection Complete!" & vbNewLine & vbNewLine & _
           "Records Analyzed: " & Format(lastRow - 1, "#,##0") & vbNewLine & _
           "Time Elapsed: " & Format(Timer - startTime, "0.0") & " seconds" & vbNewLine & vbNewLine & _
           "See 'Dashboard' sheet for summary.", vbInformation, "AP Anomaly Detector"

End Sub

Sub CreateDashboard()
    Call CreateDashboard(0)
End Sub

Sub CreateDashboard(totalRecords As Long)
    
    Dim wsDash As Worksheet
    Dim wsData As Worksheet
    Dim lastRow As Long
    Dim highCount As Long, medCount As Long, lowCount As Long, cleanCount As Long
    Dim dupCount As Long, roundCount As Long, weekendCount As Long
    Dim riskCol As Long
    
    Set wsData = ThisWorkbook.Worksheets("AP_Transactions")
    
    If totalRecords = 0 Then
        lastRow = wsData.Cells(wsData.Rows.Count, "A").End(xlUp).Row
        totalRecords = lastRow - 1
    End If
    
    ' Find the RISK_LEVEL column
    riskCol = 0
    Dim c As Long
    For c = 1 To wsData.Cells(1, wsData.Columns.Count).End(xlToLeft).Column
        If wsData.Cells(1, c).Value = "RISK_LEVEL" Then
            riskCol = c
            Exit For
        End If
    Next c
    
    If riskCol = 0 Then
        MsgBox "Please run anomaly detection first.", vbExclamation
        Exit Sub
    End If
    
    ' Count risk levels
    highCount = Application.WorksheetFunction.CountIf(wsData.Columns(riskCol), "HIGH")
    medCount = Application.WorksheetFunction.CountIf(wsData.Columns(riskCol), "MEDIUM")
    lowCount = Application.WorksheetFunction.CountIf(wsData.Columns(riskCol), "LOW")
    cleanCount = Application.WorksheetFunction.CountIf(wsData.Columns(riskCol), "CLEAN")
    
    ' Count anomaly types
    dupCount = Application.WorksheetFunction.CountIf(wsData.Columns(riskCol - 4), 1)
    roundCount = Application.WorksheetFunction.CountIf(wsData.Columns(riskCol - 3), 1)
    weekendCount = Application.WorksheetFunction.CountIf(wsData.Columns(riskCol - 2), 1)
    
    ' Delete existing dashboard
    On Error Resume Next
    ThisWorkbook.Worksheets("Dashboard").Delete
    On Error GoTo 0
    
    ' Create dashboard sheet
    Set wsDash = ThisWorkbook.Worksheets.Add(Before:=ThisWorkbook.Worksheets(1))
    wsDash.Name = "Dashboard"
    
    ' Title
    wsDash.Range("B2").Value = "AP INVOICE ANOMALY DETECTION"
    With wsDash.Range("B2")
        .Font.Size = 24
        .Font.Bold = True
        .Font.Color = RGB(0, 102, 204)
    End With
    
    wsDash.Range("B3").Value = "Executive Summary Dashboard"
    wsDash.Range("B3").Font.Size = 14
    wsDash.Range("B3").Font.Color = RGB(128, 128, 128)
    
    wsDash.Range("B4").Value = "Generated: " & Format(Now, "mmmm d, yyyy h:mm AM/PM")
    wsDash.Range("B4").Font.Italic = True
    
    ' Summary Box
    wsDash.Range("B7").Value = "TOTAL RECORDS ANALYZED"
    wsDash.Range("B7").Font.Bold = True
    wsDash.Range("B8").Value = Format(totalRecords, "#,##0")
    wsDash.Range("B8").Font.Size = 36
    wsDash.Range("B8").Font.Bold = True
    
    ' Risk Distribution
    wsDash.Range("B11").Value = "RISK DISTRIBUTION"
    wsDash.Range("B11").Font.Bold = True
    wsDash.Range("B11").Font.Size = 14
    
    wsDash.Range("B13").Value = "HIGH RISK"
    wsDash.Range("C13").Value = highCount
    wsDash.Range("D13").Value = Format(highCount / totalRecords, "0.0%")
    wsDash.Range("B13").Interior.Color = RGB(255, 0, 0)
    wsDash.Range("B13").Font.Color = RGB(255, 255, 255)
    
    wsDash.Range("B14").Value = "MEDIUM RISK"
    wsDash.Range("C14").Value = medCount
    wsDash.Range("D14").Value = Format(medCount / totalRecords, "0.0%")
    wsDash.Range("B14").Interior.Color = RGB(255, 192, 0)
    
    wsDash.Range("B15").Value = "LOW RISK"
    wsDash.Range("C15").Value = lowCount
    wsDash.Range("D15").Value = Format(lowCount / totalRecords, "0.0%")
    wsDash.Range("B15").Interior.Color = RGB(255, 255, 0)
    
    wsDash.Range("B16").Value = "CLEAN"
    wsDash.Range("C16").Value = cleanCount
    wsDash.Range("D16").Value = Format(cleanCount / totalRecords, "0.0%")
    wsDash.Range("B16").Interior.Color = RGB(146, 208, 80)
    
    ' Anomaly Breakdown
    wsDash.Range("F11").Value = "ANOMALY BREAKDOWN"
    wsDash.Range("F11").Font.Bold = True
    wsDash.Range("F11").Font.Size = 14
    
    wsDash.Range("F13").Value = "Potential Duplicates"
    wsDash.Range("G13").Value = dupCount
    wsDash.Range("H13").Value = Format(dupCount / totalRecords, "0.0%")
    
    wsDash.Range("F14").Value = "Round Number Amounts"
    wsDash.Range("G14").Value = roundCount
    wsDash.Range("H14").Value = Format(roundCount / totalRecords, "0.0%")
    
    wsDash.Range("F15").Value = "Weekend Invoices"
    wsDash.Range("G15").Value = weekendCount
    wsDash.Range("H15").Value = Format(weekendCount / totalRecords, "0.0%")
    
    ' Recommendations
    wsDash.Range("B19").Value = "RECOMMENDED ACTIONS"
    wsDash.Range("B19").Font.Bold = True
    wsDash.Range("B19").Font.Size = 14
    
    wsDash.Range("B21").Value = ChrW(9679) & " HIGH RISK: Immediate review required - potential fraud or duplicate payments"
    wsDash.Range("B22").Value = ChrW(9679) & " MEDIUM RISK: Review within 48 hours - investigate unusual patterns"
    wsDash.Range("B23").Value = ChrW(9679) & " LOW RISK: Batch review weekly - minor flags for awareness"
    
    ' Format columns
    wsDash.Columns("B:H").AutoFit
    wsDash.Columns("C").ColumnWidth = 12
    wsDash.Columns("G").ColumnWidth = 12
    
    wsDash.Activate

End Sub

Sub FilterHighRisk()
    Dim ws As Worksheet
    Dim riskCol As Long
    Dim c As Long
    
    Set ws = ThisWorkbook.Worksheets("AP_Transactions")
    
    For c = 1 To ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column
        If ws.Cells(1, c).Value = "RISK_LEVEL" Then
            riskCol = c
            Exit For
        End If
    Next c
    
    If riskCol = 0 Then
        MsgBox "Please run anomaly detection first.", vbExclamation
        Exit Sub
    End If
    
    ws.Activate
    If ws.AutoFilterMode Then ws.AutoFilterMode = False
    ws.UsedRange.AutoFilter Field:=riskCol, Criteria1:="HIGH"
    
    MsgBox "Showing HIGH RISK records only." & vbNewLine & _
           "Clear filter to see all records.", vbInformation

End Sub

Sub ClearFilters()
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets("AP_Transactions")
    If ws.AutoFilterMode Then ws.AutoFilterMode = False
    MsgBox "All filters cleared.", vbInformation
End Sub
