/*
The latest version of this package is available at:
<http://github.com/jantman/biweeklybudget>

################################################################################
Copyright 2016 Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>

    This file is part of biweeklybudget, also known as biweeklybudget.

    biweeklybudget is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    biweeklybudget is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with biweeklybudget.  If not, see <http://www.gnu.org/licenses/>.

The Copyright and Authors attributions contained herein may not be removed or
otherwise altered, except to add the Author attribution of a contributor to
this work. (Additional Terms pursuant to Section 7b of the AGPL v3)
################################################################################
While not legally required, I sincerely request that anyone who finds
bugs please submit them at <https://github.com/jantman/biweeklybudget> or
to me via email, and that you send any contributions or improvements
either as a pull request on GitHub, or to me via email.
################################################################################

AUTHORS:
Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
################################################################################
*/

/**
 * Generate the HTML for the form on the Modal
 */
function budgetTransferDivForm() {
    var frm = '<form role="form" id="budgetTransferForm">';
    // date
    frm += '<div class="form-group" id="budg_txfr_frm_group_date">';
    frm += '<label for="budg_txfr_frm_date" class="control-label">Date</label><div class="input-group date" id="budg_txfr_frm_group_date_input"><span class="input-group-addon"><i class="fa fa-calendar fa-fw"></i></span><input class="form-control" id="budg_txfr_frm_date" name="date" type="text" size="12" maxlength="10"></div>';
    frm += '</div>\n';
    // amount
    frm += '<div class="form-group"><label for="budg_txfr_frm_amount" class="control-label">Amount</label><div class="input-group"><span class="input-group-addon">$</span><input type="text" class="form-control" id="budg_txfr_frm_amount" name="amount"></div><p class="help-block">Transfer amount relative to from account; must be positive.</p></div>\n';
    // account
    frm += '<div class="form-group"><label for="budg_txfr_frm_account" class="control-label">Account</label>';
    frm += '<select id="budg_txfr_frm_account" name="account" class="form-control">';
    frm += '<option value="None" selected="selected"></option>';
    Object.keys(acct_names_to_id).forEach(function (key) {
        frm += '<option value="' + acct_names_to_id[key] + '">' + key + '</option>';
    });
    frm += '</select>';
    frm += '</div>\n';
    // from budget
    frm += '<div class="form-group"><label for="budg_txfr_frm_from_budget" class="control-label">From Budget</label>';
    frm += '<select id="budg_txfr_frm_from_budget" name="from_budget" class="form-control">';
    frm += '<option value="None" selected="selected"></option>';
    Object.keys(budget_names_to_id).forEach(function (key) {
        frm += '<option value="' + budget_names_to_id[key] + '">' + key + '</option>';
    });
    frm += '</select>';
    frm += '</div>\n';
    // to budget
    frm += '<div class="form-group"><label for="budg_txfr_frm_to_budget" class="control-label">To Budget</label>';
    frm += '<select id="budg_txfr_frm_to_budget" name="to_budget" class="form-control">';
    frm += '<option value="None" selected="selected"></option>';
    Object.keys(budget_names_to_id).forEach(function (key) {
        frm += '<option value="' + budget_names_to_id[key] + '">' + key + '</option>';
    });
    frm += '</select>';
    frm += '</div>\n';
    // notes
    frm += '<div class="form-group"><label for="budg_txfr_frm_notes" class="control-label">Notes</label><input class="form-control" id="budg_txfr_frm_notes" name="notes" type="text"></div>\n';
    frm += '</form>\n';
    return frm;
}

/**
 * Show the modal popup for transferring between budgets.
 * Uses :js:func:`budgetTransferDivForm` to generate the form.
 */
function budgetTransferModal() {
    $('#modalBody').empty();
    $('#modalBody').append(budgetTransferDivForm());
    $('#budg_txfr_frm_date').val(isoformat(new Date()));
    $('#budg_txfr_frm_group_date_input').datepicker({
        todayBtn: "linked",
        autoclose: true,
        todayHighlight: true,
        format: 'yyyy-mm-dd'
    });
    $('#modalSaveButton').off();
    $('#modalSaveButton').click(function() {
        handleForm('modalBody', 'budgetTransferForm', '/forms/budget_transfer', null);
    }).show();
    $('#modalLabel').text('Budget Transfer');
    $('#budg_txfr_frm_account option[value=' + default_account_id + ']').prop('selected', 'selected').change();
    $("#modalDiv").modal('show');
}
