<?php
/**
 * LogiFlow CRM - Theme Definition
 * Tema customizado para transportadoras
 */

if (!defined('sugarEntry') || !sugarEntry) die('Not A Valid Entry Point');

$themedef = array(
    'name' => 'LogiFlow',
    'description' => 'Tema LogiFlow CRM - Sistema para Transportadoras',
    'version' => array(
        'regex_matches' => array('.'),
    ),
    'colors' => array(
        '#1e40af', // Primary Blue
        '#0891b2', // Secondary Cyan
        '#10b981', // Success Green
        '#f59e0b', // Warning Amber
        '#ef4444', // Danger Red
    ),
    'fonts' => array(
        'Inter',
        'Roboto',
        'sans-serif',
    ),
    'group_tabs' => true,
    'classic' => false,
    'configurable' => false,
    'config_options' => array(
        'display_sidebar' => true,
        'collapsible_sidebar' => true,
    ),
    'parentTheme' => 'SuiteP',
);
