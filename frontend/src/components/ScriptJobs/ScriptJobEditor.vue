<template>
  <a-modal :open="open" :title="job ? '编辑脚本作业' : '新建脚本作业'" :width="760" :confirm-loading="saving" ok-text="保存作业"
    :mask-closable="false" :destroy-on-close="true" @cancel="close" @ok="save">
    <a-alert v-if="error" :message="error" type="error" show-icon class="editor-alert" />
    <a-form layout="vertical">
      <a-form-item label="作业名称" required><a-input v-model:value="form.name" :maxlength="255" placeholder="例如：构建发布包" :disabled="saving" /></a-form-item>
      <a-form-item label="执行节点" required extra="仅列出你有权使用的节点。离线节点可保存，提交后将等待连接。">
        <a-select v-model:value="form.environmentId" :options="nodeOptions" :disabled="saving" placeholder="选择 Agent 节点" show-search option-filter-prop="label" />
      </a-form-item>
      <a-alert v-if="selectedNode?.isOnline && !selectedNode.supportsScriptJobs" type="warning" show-icon message="此节点需要升级 Agent 才能执行脚本作业。" class="editor-alert" />
      <a-form-item label="执行方式" required><a-radio-group v-model:value="form.mode" :disabled="saving"><a-radio-button value="shell">Shell</a-radio-button><a-radio-button value="python">Python</a-radio-button><a-radio-button value="command">命令 + 参数</a-radio-button></a-radio-group></a-form-item>
      <a-form-item v-if="form.mode !== 'command'" label="脚本内容" required :extra="form.mode === 'python' ? '使用节点上的 Python 执行；脚本上限 64 KiB。' : '使用节点上的 Shell 执行；脚本上限 64 KiB。'">
        <a-textarea v-model:value="form.script" :rows="10" :maxlength="65536" class="code-input" spellcheck="false" :disabled="saving" :placeholder="form.mode === 'python' ? 'print(123)' : 'echo Hello ATS'" />
      </a-form-item>
      <a-form-item v-else label="可执行文件" required extra="填写可执行文件名称或路径，例如 npm。参数在下方单独填写，保留空格，不经 Shell 拼接。">
        <a-input v-model:value="form.command" :maxlength="4096" :disabled="saving" placeholder="例如 npm 或 python3" />
      </a-form-item>
      <a-form-item label="参数（按顺序传入）" extra="Shell、Python 和命令均支持参数。每行作为一个参数，空格和空字符串会原样传入。">
        <div v-for="(_, index) in form.args" :key="index" class="argument-row">
          <a-input v-model:value="form.args[index]" :aria-label="`参数 ${index + 1}`" :disabled="saving" :maxlength="8192" placeholder="一个参数；可包含空格" />
          <a-button :disabled="saving" :aria-label="`移除参数 ${index + 1}`" @click="form.args.splice(index, 1)">移除</a-button>
        </div>
        <a-button size="small" :disabled="saving || form.args.length >= 128" @click="form.args.push('')">添加参数</a-button>
      </a-form-item>
      <div class="editor-grid">
        <a-form-item label="工作目录" extra="相对于节点工作空间。留空使用本次运行的隔离目录。">
          <a-input v-model:value="form.workDir" :maxlength="500" :disabled="saving" placeholder="例如 builds/my-project" />
        </a-form-item>
        <a-form-item label="执行超时（秒）" required extra="1–86400 秒；到期后 Agent 停止进程。">
          <a-input-number v-model:value="form.timeoutSeconds" :min="1" :max="86400" :precision="0" :disabled="saving" />
        </a-form-item>
      </div>
      <p class="hint">每次运行固定保存当时的配置，之后编辑作业不会改变已有运行。</p>
    </a-form>
  </a-modal>
</template>
<script setup lang="ts">
import type { ScriptJob, ScriptNode } from '@/api/scriptJobs'
import { useScriptJobEditor } from './useScriptJobEditor'
const props = defineProps<{ open: boolean; projectId: string; job: ScriptJob | null; nodes: ScriptNode[] }>()
const emit = defineEmits<{ close: []; saved: [job: ScriptJob] }>()
const { form, saving, error, selectedNode, nodeOptions, close, save } = useScriptJobEditor(props, { close: () => emit('close'), saved: job => emit('saved', job) })
</script>
<style scoped>
.editor-alert { margin-bottom: 16px; }
.argument-row { display: flex; gap: 8px; margin-bottom: 8px; }
.editor-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 16px; }
.code-input { font-family: monospace; tab-size: 2; }
.hint { color: var(--ms-text-secondary); font-size: 12px; }
@media (max-width: 600px) { .editor-grid { grid-template-columns: 1fr; gap: 0; } }
</style>
