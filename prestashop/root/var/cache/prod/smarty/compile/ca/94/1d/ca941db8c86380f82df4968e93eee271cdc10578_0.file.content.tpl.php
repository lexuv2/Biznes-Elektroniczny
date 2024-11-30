<?php
/* Smarty version 3.1.43, created on 2024-11-30 12:12:12
  from '/var/www/html/admin6787apny1/themes/default/template/content.tpl' */

/* @var Smarty_Internal_Template $_smarty_tpl */
if ($_smarty_tpl->_decodeProperties($_smarty_tpl, array (
  'version' => '3.1.43',
  'unifunc' => 'content_674af30c145df3_40495274',
  'has_nocache_code' => false,
  'file_dependency' => 
  array (
    'ca941db8c86380f82df4968e93eee271cdc10578' => 
    array (
      0 => '/var/www/html/admin6787apny1/themes/default/template/content.tpl',
      1 => 1732961288,
      2 => 'file',
    ),
  ),
  'includes' => 
  array (
  ),
),false)) {
function content_674af30c145df3_40495274 (Smarty_Internal_Template $_smarty_tpl) {
?><div id="ajax_confirmation" class="alert alert-success hide"></div>
<div id="ajaxBox" style="display:none"></div>

<div class="row">
	<div class="col-lg-12">
		<?php if ((isset($_smarty_tpl->tpl_vars['content']->value))) {?>
			<?php echo $_smarty_tpl->tpl_vars['content']->value;?>

		<?php }?>
	</div>
</div>
<?php }
}
