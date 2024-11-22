<?php
/* Smarty version 3.1.43, created on 2024-11-21 23:17:21
  from '/var/www/html/admin6787apny1/themes/default/template/content.tpl' */

/* @var Smarty_Internal_Template $_smarty_tpl */
if ($_smarty_tpl->_decodeProperties($_smarty_tpl, array (
  'version' => '3.1.43',
  'unifunc' => 'content_673fb1712d6ad6_44262773',
  'has_nocache_code' => false,
  'file_dependency' => 
  array (
    'ca941db8c86380f82df4968e93eee271cdc10578' => 
    array (
      0 => '/var/www/html/admin6787apny1/themes/default/template/content.tpl',
      1 => 1732226167,
      2 => 'file',
    ),
  ),
  'includes' => 
  array (
  ),
),false)) {
function content_673fb1712d6ad6_44262773 (Smarty_Internal_Template $_smarty_tpl) {
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
